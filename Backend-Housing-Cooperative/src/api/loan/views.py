from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from config.permissions import IsAdminUserCustom


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

from .models import Loan, LoanRepaymentSchedule, LoanStatus
from .serializers import (
    LoanPreviewSerializer, LoanApplicationSerializer,
    LoanDetailSerializer, LoanListSerializer, AdminLoanDetailSerializer,LoanRejectSerializer,
    check_loan_eligibility,
)
from .services import disburse_loan, process_repayment


class LoanPreviewView(APIView):
    """
    POST /loans/preview/
    Returns repayment breakdown without creating a loan.
    Body: { "principal": 200000, "tenure_months": 6 }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        principal = serializer.validated_data["principal"]
        tenure_months = serializer.validated_data["tenure_months"]

        is_eligible, reason, max_loan_amount = check_loan_eligibility(request.user)
        if not is_eligible:
            return Response({"error": reason}, status=status.HTTP_403_FORBIDDEN)

        if principal > max_loan_amount:
            return Response(
                {"error": f"Maximum loan amount is ₦{max_loan_amount:,.2f} (2× your balance)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = Loan.calculate_summary(Decimal(str(principal)), tenure_months)
        return Response(summary, status=status.HTTP_200_OK)


class LoanApplyView(APIView):
    """POST /loans/apply/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanApplicationSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        loan = serializer.save(user=request.user)
        return Response(LoanDetailSerializer(loan).data, status=status.HTTP_201_CREATED)


class UserLoanListView(APIView):
    """GET /loans/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loan.objects.filter(user=request.user)
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(loans, request)
        return paginator.get_paginated_response(LoanListSerializer(page, many=True).data)


class UserLoanDetailView(APIView):
    """GET /loans/<uid>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid, user=request.user)
        return Response(LoanDetailSerializer(loan).data)


class LoanRepayView(APIView):
    """
    POST /loans/<uid>/repay/

    Immediately deducts the current month's installment from the user's
    wallet — no need to wait for the end-of-month scheduler.

    The scheduler will skip any installment already marked is_paid=True,
    so early payment is fully safe and idempotent.

    Optional body: { "installment_number": 3 }
    If omitted, defaults to the earliest unpaid installment due this month
    (falling back to the next upcoming unpaid installment).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid, user=request.user)

        if loan.status != LoanStatus.ACTIVE:
            return Response(
                {"error": f"Only ACTIVE loans can be repaid. Current status: {loan.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        installment_number = request.data.get("installment_number")

        if installment_number is not None:
            # User explicitly chose an installment
            try:
                installment_number = int(installment_number)
            except (TypeError, ValueError):
                return Response(
                    {"error": "installment_number must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            schedule = get_object_or_404(
                LoanRepaymentSchedule,
                loan=loan,
                installment_number=installment_number,
            )
        else:
            # Auto-select: earliest unpaid installment due this month,
            # or next upcoming unpaid installment if none due this month.
            from django.utils import timezone
            today = timezone.now().date()
            schedule = (
                loan.schedule
                .filter(is_paid=False, due_date__year=today.year, due_date__month=today.month)
                .order_by("installment_number")
                .first()
                or loan.schedule
                .filter(is_paid=False)
                .order_by("installment_number")
                .first()
            )
            if not schedule:
                return Response(
                    {"error": "No outstanding installments found. Your loan may already be fully paid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        result = process_repayment(schedule)

        # Map internal status to HTTP status
        if result["status"] == "already_paid":
            return Response(result, status=status.HTTP_200_OK)

        if result["status"] == "insufficient_funds":
            return Response(result, status=status.HTTP_402_PAYMENT_REQUIRED)

        # success — return updated loan detail so the client state is fresh
        loan.refresh_from_db()
        return Response(
            {
                **result,
                "loan": LoanDetailSerializer(loan).data,
            },
            status=status.HTTP_200_OK,
        )


class AdminLoanListView(APIView):
    """GET /admin/loans/?status=PENDING"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        qs = Loan.objects.select_related("user").all()
        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter.upper())
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(AdminLoanDetailSerializer(page, many=True).data)


class AdminLoanDetailView(APIView):
    """GET /admin/loans/<uid>/"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid)
        return Response(AdminLoanDetailSerializer(loan).data)


class AdminApproveLoanView(APIView):
    """POST /admin/loans/<uid>/approve/"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid)

        if loan.status != LoanStatus.PENDING:
            return Response(
                {"error": f"Only PENDING loans can be approved. Current: {loan.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        disburse_loan(loan, request.user)
        return Response(AdminLoanDetailSerializer(loan).data, status=status.HTTP_200_OK)


class AdminRejectLoanView(APIView):
    """POST /admin/loans/<uid>/reject/  Body: { "rejection_reason": "..." }"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        # Validate first, before touching the DB
        reject_serializer = LoanRejectSerializer(data=request.data)
        reject_serializer.is_valid(raise_exception=True)

        loan = get_object_or_404(Loan, uid=uid)

        if loan.status != LoanStatus.PENDING:
            return Response(
                {"error": "Only PENDING loans can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        loan.status = LoanStatus.REJECTED
        loan.rejection_reason = reject_serializer.validated_data["rejection_reason"]
        loan.approved_by = request.user
        loan.approved_at = timezone.now()
        loan.save(update_fields=["status", "rejection_reason", "approved_by", "approved_at", "updated_at"])
        return Response(AdminLoanDetailSerializer(loan).data, status=status.HTTP_200_OK)
