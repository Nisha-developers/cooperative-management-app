from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from config.permissions import IsAdminUserCustom

from .models import Loan, LoanStatus
from .serializers import (
    LoanPreviewSerializer, LoanApplicationSerializer,
    LoanDetailSerializer, LoanListSerializer, AdminLoanDetailSerializer,
)
from .services import disburse_loan


class LoanPreviewView(APIView):
    """
    POST /loans/preview/
    No loan is created. Returns full repayment breakdown before applying.
    Body: { "principal": 200000, "tenure_months": 6 }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        principal = serializer.validated_data["principal"]
        tenure_months = serializer.validated_data["tenure_months"]

        # Eligibility check
        try:
            wallet = request.user.wallet
        except Exception:
            return Response({"error": "No wallet found."}, status=status.HTTP_400_BAD_REQUEST)

        max_allowed = wallet.balance * 2
        if principal > max_allowed:
            return Response(
                {"error": f"Maximum loan amount is ₦{max_allowed:,.2f} (2× your balance)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = Loan.calculate_summary(Decimal(str(principal)), tenure_months)
        return Response(summary, status=status.HTTP_200_OK)


class LoanApplyView(APIView):
    """
    POST /loans/apply/
    Creates a PENDING loan for admin review.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanApplicationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        loan = serializer.save(user=request.user)
        return Response(LoanDetailSerializer(loan).data, status=status.HTTP_201_CREATED)


class UserLoanListView(APIView):
    """GET /loans/ — current user's loan history"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loan.objects.filter(user=request.user)
        return Response(LoanListSerializer(loans, many=True).data)


class UserLoanDetailView(APIView):
    """GET /loans/<uid>/ — loan detail + schedule"""
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid, user=request.user)
        return Response(LoanDetailSerializer(loan).data)


# ── Admin ──────────────────────────────────────────────────────────────────

class AdminLoanListView(APIView):
    """GET /admin/loans/?status=PENDING"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        qs = Loan.objects.select_related("user").all()
        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter.upper())
        return Response(AdminLoanDetailSerializer(qs, many=True).data)


class AdminLoanDetailView(APIView):
    """GET /admin/loans/<uid>/"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid)
        return Response(AdminLoanDetailSerializer(loan).data)


class AdminApproveLoanView(APIView):
    """
    POST /admin/loans/<uid>/approve/
    Disburses principal to wallet and generates repayment schedule.
    """
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
    """POST /admin/loans/<uid>/reject/  Body: { "remark": "..." }"""
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        loan = get_object_or_404(Loan, uid=uid)

        if loan.status != LoanStatus.PENDING:
            return Response(
                {"error": "Only PENDING loans can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        loan.status = LoanStatus.REJECTED
        loan.remark = request.data.get("remark", "")
        loan.approved_by = request.user
        loan.approved_at = __import__("django.utils.timezone", fromlist=["timezone"]).timezone.now()
        loan.save()
        return Response(AdminLoanDetailSerializer(loan).data, status=status.HTTP_200_OK)
