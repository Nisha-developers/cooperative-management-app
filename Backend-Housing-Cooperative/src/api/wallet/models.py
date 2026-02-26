from decimal import Decimal
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


def generate_wallet_reference():
    return f"WTX-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


class WalletTransactionType(models.TextChoices):
    CREDIT = "CREDIT", "Credit"
    DEBIT = "DEBIT", "Debit"


class WalletTransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    REJECTED = "REJECTED", "Rejected"


class WalletTransactionSource(models.TextChoices):
    INITIAL_ADMIN_SET = "INITIAL_ADMIN_SET", "Initial admin set"
    USER_TOPUP = "USER_TOPUP", "User top-up"
    ADMIN_ADJUSTMENT = "ADMIN_ADJUSTMENT", "Admin adjustment"
    WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
    PURCHASE = "PURCHASE", "Purchase"


class Wallet(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="wallet",
        on_delete=models.CASCADE,
    )

    # cached balance (fast reads)
    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallet"
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return f"Wallet({self.user_id})"


class WalletTransaction(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    wallet = models.ForeignKey(
        Wallet,
        related_name="transactions",
        on_delete=models.CASCADE,
    )

    type = models.CharField(max_length=10, choices=WalletTransactionType.choices)
    source = models.CharField(max_length=30, choices=WalletTransactionSource.choices)
    status = models.CharField(
        max_length=10,
        choices=WalletTransactionStatus.choices,
        default=WalletTransactionStatus.PENDING,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    reference = models.CharField(
        max_length=120,
        unique=True,
        default=generate_wallet_reference,
        db_index=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="wallet_transactions_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="wallet_transactions_confirmed",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallet_transaction"
        ordering = ["-created_on"]
        indexes = [
            models.Index(fields=["wallet", "status"]),
            models.Index(fields=["source", "status"]),
            models.Index(fields=["wallet", "created_on"]),
        ]

    def __str__(self) -> str:
        return f"{self.reference} | {self.type} {self.amount} ({self.status})"