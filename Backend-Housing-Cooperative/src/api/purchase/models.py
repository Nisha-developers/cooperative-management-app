import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class PurchaseStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"           # Approved & installment ongoing (or outright paid)
    COMPLETED = "COMPLETED", "Completed"  # All installments cleared / outright confirmed
    REJECTED = "REJECTED", "Rejected"
    DEFAULTED = "DEFAULTED", "Defaulted"


class PurchaseType(models.TextChoices):
    OUTRIGHT = "OUTRIGHT", "Outright"
    INSTALLMENT = "INSTALLMENT", "Installment"


class Purchase(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="purchases",
        on_delete=models.CASCADE,
    )
    listing = models.ForeignKey(
        "listings.Listing",
        related_name="purchases",
        on_delete=models.PROTECT,   # never silently delete a property with open purchases
    )

    purchase_type = models.CharField(max_length=15, choices=PurchaseType.choices)

    # ── Financial snapshot at the time of application ──────────────────────────
    property_price = models.DecimalField(max_digits=14, decimal_places=2)

    # Installment-specific fields (null for OUTRIGHT)
    initial_deposit = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
        help_text="Deposit paid upfront to kick off the installment plan",
    )
    balance_after_deposit = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
    )
    tenure_months = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Installment duration in months",
    )
    monthly_installment = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
    )
    total_repayable = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
        help_text="balance_after_deposit (no interest — property purchase, not a loan)",
    )

    status = models.CharField(
        max_length=20, choices=PurchaseStatus.choices, default=PurchaseStatus.PENDING
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="purchases_approved",
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Purchase({self.uid}) — {self.user} — {self.listing.title} [{self.status}]"

    @staticmethod
    def calculate_installment_summary(
        property_price: Decimal,
        initial_deposit: Decimal,
        tenure_months: int,
    ) -> dict:
        """
        Property installments carry NO interest — the buyer pays exactly the
        property price.  The deposit is deducted up-front; the remaining
        balance is spread evenly across the tenure.
        """
        balance = (property_price - initial_deposit).quantize(Decimal("0.01"))
        monthly = (balance / tenure_months).quantize(Decimal("0.01"))
        return {
            "property_price": property_price,
            "initial_deposit": initial_deposit,
            "balance_after_deposit": balance,
            "tenure_months": tenure_months,
            "monthly_installment": monthly,
            "total_repayable": balance,
        }


class PurchaseInstallmentSchedule(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    purchase = models.ForeignKey(
        Purchase, related_name="schedule", on_delete=models.CASCADE
    )

    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )

    is_paid = models.BooleanField(default=False)
    is_overdue = models.BooleanField(
        default=False,
        help_text="Flagged by the scheduler when due_date passes without payment",
    )

    paid_at = models.DateTimeField(null=True, blank=True)
    wallet_transaction = models.OneToOneField(
        "wallet.WalletTransaction",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="purchase_installment",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["installment_number"]
        unique_together = [("purchase", "installment_number")]

    def __str__(self):
        return f"Installment {self.installment_number} for Purchase {self.purchase.uid}"