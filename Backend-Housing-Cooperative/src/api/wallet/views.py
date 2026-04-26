from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsAdminUserCustom
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Wallet,
    WalletPaymentProof,
    WalletTransaction,
    WalletTransactionSource,
    WalletTransactionStatus,
    WalletTransactionType,
)
from api.utils.cloudinary import upload_payment_proof
from .serializers import (
    AdminProofUploadSerializer,
    ClientProofUploadSerializer,
    CreditTransactionSerializer,
    DebitTransactionSerializer,
    TransactionRejectSerializer,
    TransactionReviewSerializer,
    WalletPaymentProofSerializer,
    WalletSerializer,
    WalletSummarySerializer,
    WalletTransactionSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


def _requires_client_proof(tx: WalletTransaction) -> bool:
    return (
        tx.source == WalletTransactionSource.TRANSFER
        and tx.type == WalletTransactionType.CREDIT
    )


def _requires_admin_proof(tx: WalletTransaction) -> bool:
    return (
        tx.source == WalletTransactionSource.TRANSFER
        and tx.type == WalletTransactionType.DEBIT
    )


def _get_wallet_or_404(user) -> Wallet:
    try:
        return Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        raise NotFound("Wallet not found.")


def _get_transaction_or_404(uid: str) -> WalletTransaction:
    try:
        return WalletTransaction.objects.select_related("wallet").get(uid=uid)
    except WalletTransaction.DoesNotExist:
        raise NotFound("Transaction not found.")


# ---------------------------------------------------------------------------
# Client views
# ---------------------------------------------------------------------------

class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, full=False):
        wallet = _get_wallet_or_404(request.user)
        SerializerClass = WalletSerializer if full else WalletSummarySerializer
        return Response(SerializerClass(wallet).data)


class WalletTransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = _get_wallet_or_404(request.user)
        qs = wallet.transactions.select_related("payment_proof").all()

        if status_filter := request.query_params.get("status"):
            qs = qs.filter(status=status_filter.upper())

        if type_filter := request.query_params.get("type"):
            qs = qs.filter(type=type_filter.upper())

        return Response(WalletTransactionSerializer(qs, many=True).data)


class WalletTransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = _get_wallet_or_404(request.user)
        qs = (
            wallet.transactions
            .select_related("payment_proof")
            .filter(status=WalletTransactionStatus.CONFIRMED)
            .order_by("created_on")
        )

        if type_filter := request.query_params.get("type"):
            qs = qs.filter(type=type_filter.upper())

        return Response(WalletTransactionSerializer(qs, many=True).data)


class WalletCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = _get_wallet_or_404(request.user)
        serializer = CreditTransactionSerializer(
            data=request.data,
            context={"request": request, "wallet": wallet},
        )
        serializer.is_valid(raise_exception=True)
        tx = serializer.save()
        return Response(WalletTransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


class WalletDebitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = _get_wallet_or_404(request.user)
        serializer = DebitTransactionSerializer(
            data=request.data,
            context={"request": request, "wallet": wallet},
        )
        serializer.is_valid(raise_exception=True)
        tx = serializer.save()
        return Response(WalletTransactionSerializer(tx).data, status=status.HTTP_201_CREATED)


class ClientProofUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, uid):
        tx = _get_transaction_or_404(uid)
 
        if tx.wallet.user_id != request.user.pk:
            raise NotFound("Transaction not found.")
 
        if tx.status != WalletTransactionStatus.PENDING:
            raise ValidationError("Proof can only be attached to a PENDING transaction.")
 
        if not _requires_client_proof(tx):
            raise ValidationError(
                "Payment proof is only required for TRANSFER credit transactions."
            )
 
        if hasattr(tx, "payment_proof"):
            raise ValidationError("Payment proof has already been uploaded.")
 
        serializer = ClientProofUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        # ── Upload to Cloudinary ──────────────────────────────────────────────
        image_file = serializer.validated_data["image"]
        image_url = upload_payment_proof(image_file, tx.reference)
        # ─────────────────────────────────────────────────────────────────────
 
        proof = WalletPaymentProof.objects.create(
            transaction=tx,
            uploaded_by=request.user,
            image_url=image_url,
        )
        return Response(WalletPaymentProofSerializer(proof).data, status=201)


class AdminTransactionListView(APIView):
    """
    GET /admin/wallet/transactions/

    Lists all transactions. Optional filters:
      ?status=PENDING | CONFIRMED | REJECTED
      ?type=CREDIT | DEBIT
    """
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        qs = WalletTransaction.objects.select_related(
            "wallet__user", "payment_proof", "created_by"
        ).order_by("-created_on")

        if status_filter := request.query_params.get("status"):
            qs = qs.filter(status=status_filter.upper())

        if type_filter := request.query_params.get("type"):
            qs = qs.filter(type=type_filter.upper())

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(
            WalletTransactionSerializer(page, many=True).data
        )


class AdminApproveTransactionView(APIView):
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        review_serializer = TransactionReviewSerializer(data=request.data)
        review_serializer.is_valid(raise_exception=True)

        tx = _get_transaction_or_404(uid)

        if tx.status != WalletTransactionStatus.PENDING:
            raise ValidationError(
                f"Only PENDING transactions can be approved. Current status: {tx.status}"
            )

        if _requires_admin_proof(tx) and not hasattr(tx, "payment_proof"):
            raise ValidationError(
                "Upload payment proof first via POST /admin/wallet/transactions/<uid>/proof/"
            )

        wallet = tx.wallet

        with db_transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(pk=wallet.pk)

            if tx.type == WalletTransactionType.CREDIT:
                wallet.balance += tx.amount
            elif tx.type == WalletTransactionType.DEBIT:
                if wallet.balance < tx.amount:
                    raise ValidationError({"amount": "Insufficient wallet balance for this debit."})
                wallet.balance -= tx.amount

            wallet.save(update_fields=["balance", "updated_on"])

            admin_remark = review_serializer.validated_data.get("remark", "")
            if admin_remark:
                tx.remark = (
                    f"{tx.remark}\n[Admin] {admin_remark}".strip() if tx.remark
                    else f"[Admin] {admin_remark}"
                )

            tx.status = WalletTransactionStatus.CONFIRMED
            tx.confirmed_by = request.user
            tx.confirmed_at = timezone.now()
            tx.save(update_fields=["status", "confirmed_by", "confirmed_at", "remark", "updated_on"])

        return Response(WalletTransactionSerializer(tx).data, status=status.HTTP_200_OK)


class AdminRejectTransactionView(APIView):
    permission_classes = [IsAdminUserCustom]

    def post(self, request, uid):
        reject_serializer = TransactionRejectSerializer(data=request.data)
        reject_serializer.is_valid(raise_exception=True)

        tx = _get_transaction_or_404(uid)

        if tx.status != WalletTransactionStatus.PENDING:
            raise ValidationError(
                f"Only PENDING transactions can be rejected. Current status: {tx.status}"
            )

        tx.rejection_reason = reject_serializer.validated_data["rejection_reason"]
        tx.status = WalletTransactionStatus.REJECTED
        tx.confirmed_by = request.user
        tx.confirmed_at = timezone.now()
        tx.save(update_fields=["status", "confirmed_by", "confirmed_at", "rejection_reason", "updated_on"])

        return Response(WalletTransactionSerializer(tx).data, status=status.HTTP_200_OK)


class AdminProofUploadView(APIView):
    permission_classes = [IsAdminUserCustom]
    parser_classes = [MultiPartParser, FormParser]
 
    def post(self, request, uid):
        tx = _get_transaction_or_404(uid)
 
        if tx.status != WalletTransactionStatus.PENDING:
            raise ValidationError("Proof can only be attached to a PENDING transaction.")
 
        if not _requires_admin_proof(tx):
            raise ValidationError(
                "Admin proof upload is only applicable to DEBIT + TRANSFER transactions."
            )
 
        if hasattr(tx, "payment_proof"):
            raise ValidationError("Payment proof has already been uploaded for this transaction.")
 
        serializer = AdminProofUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_file = serializer.validated_data["image"]
        image_url = upload_payment_proof(image_file, tx.reference)
 
        proof = WalletPaymentProof.objects.create(
            transaction=tx,
            uploaded_by=request.user,
            image_url=image_url,
        )
        return Response(WalletPaymentProofSerializer(proof).data, status=201)
 