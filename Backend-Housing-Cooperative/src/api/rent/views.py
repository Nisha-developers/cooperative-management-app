from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsAdminUserCustom

from .models import Rent, RentStatus
from .serializers import (
    RentPreviewSerializer,
    RentApplicationSerializer,
    RentDetailSerializer,
    RentListSerializer,
    AdminRentDetailSerializer,
)
from .services import approve_rent


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class RentPreviewView(APIView):
    """
    POST /rent/preview/
    Returns cost breakdown without creating any record.
    Body: { "listing_id": "...", "duration_days": 30 }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RentPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        listing = data["listing"]
        duration_days = data["duration_days"]

        from .models import Rent
        total_cost = Rent.calculate_total(listing.price_per_day, duration_days)

        return Response({
            "listing_id": str(listing.id),
            "listing_title": listing.title,
            "price_per_day": listing.price_per_day,
            "duration_days": duration_days,
            "total_rent_cost": total_cost,
        })


class RentApplyView(APIView):
    """POST /rent/apply/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RentApplicationSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        listing = data["listing"]

        rent = Rent.objects.create(
            user=request.user,
            listing=listing,
            price_per_day=listing.price_per_day,
            duration_days=data["duration_days"],
            total_rent_cost=data["total_cost"],
        )

        # Lock the listing so it won't appear available to other applicants
        listing.mark_pending()

        from api.users.tasks import send_rent_application_received
        try:
            send_rent_application_received(
                request.user.email,
                request.user.membership_id or request.user.email,
                listing.title,
                data["duration_days"],
                data["total_cost"],
            )
        except Exception:
            pass

        return Response(RentDetailSerializer(rent).data, status=status.HTTP_201_CREATED)


class UserRentListView(APIView):
    """GET /rent/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rents = Rent.objects.filter(user=request.user).select_related("listing")
        if status_filter := request.query_params.get("status"):
            rents = rents.filter(status=status_filter.upper())
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(rents, request)
        return paginator.get_paginated_response(RentListSerializer(page, many=True).data)


class UserRentDetailView(APIView):
    """GET /rent/<uid>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        rent = get_object_or_404(Rent, uid=uid, user=request.user)
        return Response(RentDetailSerializer(rent).data)


# ── Admin views ────────────────────────────────────────────────────────────────

class AdminRentListView(APIView):
    """GET /rent/admin/?status=PENDING"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        qs = Rent.objects.select_related("user", "listing").all()
        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter.upper())
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(AdminRentDetailSerializer(page, many=True).data)


class AdminRentDetailView(APIView):
    """GET /rent/admin/<uid>/"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request, uid):
        rent = get_object_or_404(Rent, uid=uid)
        return Response(AdminRentDetailSerializer(rent).data)


class AdminApproveRentView(APIView):
    """POST /rent/admin/<uid>/approve/"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        rent = get_object_or_404(Rent, uid=uid)

        if rent.status != RentStatus.PENDING:
            return Response(
                {"error": f"Only PENDING rents can be approved. Current: {rent.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            approve_rent(rent, request.user)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        rent.refresh_from_db()

        from api.users.tasks import send_rent_approved
        try:
            send_rent_approved(
                rent.user.email,
                rent.user.membership_id or rent.user.email,
                rent.listing.title,
                rent.start_date,
                rent.end_date,
                rent.total_rent_cost,
            )
        except Exception:
            pass

        return Response(AdminRentDetailSerializer(rent).data, status=status.HTTP_200_OK)


class AdminRejectRentView(APIView):
    """POST /rent/admin/<uid>/reject/  Body: { "rejection_reason": "..." }"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        rent = get_object_or_404(Rent, uid=uid)

        if rent.status != RentStatus.PENDING:
            return Response(
                {"error": "Only PENDING rents can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rejection_reason = request.data.get("rejection_reason", "").strip()
        if not rejection_reason:
            return Response(
                {"error": "rejection_reason is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rent.status = RentStatus.REJECTED
        rent.rejection_reason = rejection_reason
        rent.approved_by = request.user
        rent.approved_at = timezone.now()
        rent.save(update_fields=["status", "rejection_reason", "approved_by", "approved_at", "updated_at"])

        # Release the listing back to available so others can apply
        rent.listing.mark_available()

        from api.users.tasks import send_rent_rejected
        try:
            send_rent_rejected(
                rent.user.email,
                rent.user.membership_id or rent.user.email,
                rent.listing.title,
                rejection_reason,
            )
        except Exception:
            pass

        return Response(AdminRentDetailSerializer(rent).data, status=status.HTTP_200_OK)
