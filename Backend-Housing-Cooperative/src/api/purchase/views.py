from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsAdminUserCustom

from .models import Purchase, PurchaseInstallmentSchedule, PurchaseStatus, PurchaseType
from .serializers import (
    PurchasePreviewSerializer,
    PurchaseApplicationSerializer,
    PurchaseDetailSerializer,
    PurchaseListSerializer,
    AdminPurchaseDetailSerializer,
)
from .services import approve_purchase, process_installment_payment


class PurchasePreviewView(APIView):
    """
    POST /purchase/preview/
    Returns a breakdown of the purchase without creating any record.

    Body (outright):
        { "listing_id": "...", "purchase_type": "OUTRIGHT" }

    Body (installment):
        {
          "listing_id": "...",
          "purchase_type": "INSTALLMENT",
          "initial_deposit": 500000,
          "tenure_months": 12
        }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PurchasePreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        listing = data["listing"]

        if data["purchase_type"] == PurchaseType.OUTRIGHT:
            return Response({
                "purchase_type": PurchaseType.OUTRIGHT,
                "property_price": listing.price,
                "amount_to_pay": listing.price,
            })

        summary = Purchase.calculate_installment_summary(
            listing.price,
            data["initial_deposit"],
            data["tenure_months"],
        )
        return Response(summary)


class PurchaseApplyView(APIView):
    """
    POST /purchase/apply/
    Submits a purchase application (PENDING until admin approves).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PurchaseApplicationSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        listing = data["listing"]

        # Build initial financial snapshot
        purchase_kwargs = {
            "user": request.user,
            "listing": listing,
            "purchase_type": data["purchase_type"],
            "property_price": listing.price,
        }

        if data["purchase_type"] == PurchaseType.INSTALLMENT:
            purchase_kwargs["initial_deposit"] = data["initial_deposit"]
            purchase_kwargs["tenure_months"] = data["tenure_months"]
            # balance_after_deposit / monthly_installment / total_repayable are
            # computed and stored when admin approves to avoid stale snapshots.

        purchase = Purchase.objects.create(**purchase_kwargs)
        return Response(
            PurchaseDetailSerializer(purchase).data,
            status=status.HTTP_201_CREATED,
        )


class UserPurchaseListView(APIView):
    """GET /purchase/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchases = Purchase.objects.filter(user=request.user).select_related("listing")
        return Response(PurchaseListSerializer(purchases, many=True).data)


class UserPurchaseDetailView(APIView):
    """GET /purchase/<uid>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        purchase = get_object_or_404(Purchase, uid=uid, user=request.user)
        return Response(PurchaseDetailSerializer(purchase).data)


class PurchasePayInstallmentView(APIView):
    """
    POST /purchase/<uid>/pay/

    Immediately pays the current month's installment from the user's wallet.
    The daily scheduler will also call process_installment_payment — it skips
    any installment already marked is_paid=True, so manual early payment is safe.

    Optional body: { "installment_number": 3 }
    If omitted, auto-selects the earliest unpaid installment due this month,
    falling back to the next upcoming unpaid installment.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, uid):
        purchase = get_object_or_404(Purchase, uid=uid, user=request.user)

        if purchase.status != PurchaseStatus.ACTIVE:
            return Response(
                {"error": f"Only ACTIVE purchases can be paid. Current status: {purchase.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if purchase.purchase_type != PurchaseType.INSTALLMENT:
            return Response(
                {"error": "Outright purchases have no installment schedule to pay."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        installment_number = request.data.get("installment_number")

        if installment_number is not None:
            try:
                installment_number = int(installment_number)
            except (TypeError, ValueError):
                return Response(
                    {"error": "installment_number must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            schedule = get_object_or_404(
                PurchaseInstallmentSchedule,
                purchase=purchase,
                installment_number=installment_number,
            )
        else:
            today = timezone.now().date()
            schedule = (
                purchase.schedule
                .filter(is_paid=False, due_date__year=today.year, due_date__month=today.month)
                .order_by("installment_number")
                .first()
                or purchase.schedule
                .filter(is_paid=False)
                .order_by("installment_number")
                .first()
            )
            if not schedule:
                return Response(
                    {"error": "No outstanding installments. This purchase may already be fully paid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        result = process_installment_payment(schedule)

        if result["status"] == "already_paid":
            return Response(result, status=status.HTTP_200_OK)

        if result["status"] == "insufficient_funds":
            return Response(result, status=status.HTTP_402_PAYMENT_REQUIRED)

        purchase.refresh_from_db()
        return Response(
            {
                **result,
                "purchase": PurchaseDetailSerializer(purchase).data,
            },
            status=status.HTTP_200_OK,
        )


# ── Admin views ────────────────────────────────────────────────────────────────

class AdminPurchaseListView(APIView):
    """GET /purchase/admin/?status=PENDING"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        qs = Purchase.objects.select_related("user", "listing").all()
        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter.upper())
        return Response(AdminPurchaseDetailSerializer(qs, many=True).data)


class AdminPurchaseDetailView(APIView):
    """GET /purchase/admin/<uid>/"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request, uid):
        purchase = get_object_or_404(Purchase, uid=uid)
        return Response(AdminPurchaseDetailSerializer(purchase).data)


class AdminApprovePurchaseView(APIView):
    """POST /purchase/admin/<uid>/approve/"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        purchase = get_object_or_404(Purchase, uid=uid)

        if purchase.status != PurchaseStatus.PENDING:
            return Response(
                {"error": f"Only PENDING purchases can be approved. Current: {purchase.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        approve_purchase(purchase, request.user)
        purchase.refresh_from_db()
        return Response(AdminPurchaseDetailSerializer(purchase).data, status=status.HTTP_200_OK)


class AdminRejectPurchaseView(APIView):
    """POST /purchase/admin/<uid>/reject/  Body: { "remark": "..." }"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        purchase = get_object_or_404(Purchase, uid=uid)

        if purchase.status != PurchaseStatus.PENDING:
            return Response(
                {"error": "Only PENDING purchases can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        purchase.status = PurchaseStatus.REJECTED
        purchase.remark = request.data.get("remark", "")
        purchase.approved_by = request.user
        purchase.approved_at = timezone.now()
        purchase.save()

        return Response(AdminPurchaseDetailSerializer(purchase).data, status=status.HTTP_200_OK)