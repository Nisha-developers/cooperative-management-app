import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class RentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"


class Rent(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rents",
        on_delete=models.CASCADE,
    )
    listing = models.ForeignKey(
        "listings.Listing",
        related_name="rents",
        on_delete=models.PROTECT,
    )

    # Financial snapshot at application time
    price_per_day = models.DecimalField(max_digits=14, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Number of days the user wants to rent")
    total_rent_cost = models.DecimalField(max_digits=14, decimal_places=2)

    # Rental period (set on approval/payment)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20, choices=RentStatus.choices, default=RentStatus.PENDING
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rents_approved",
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(blank=True, default="")
    rejection_reason = models.TextField(blank=True, default="")

    wallet_transaction = models.OneToOneField(
        "wallet.WalletTransaction",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="rent",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rent({self.uid}) — {self.user} — {self.listing.title} [{self.status}]"

    @staticmethod
    def calculate_total(price_per_day: Decimal, duration_days: int) -> Decimal:
        return (price_per_day * duration_days).quantize(Decimal("0.01"))
