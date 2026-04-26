import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class LoanStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    REJECTED = "REJECTED", "Rejected"
    DEFAULTED = "DEFAULTED", "Defaulted"


MONTHLY_INTEREST_RATE = Decimal("0.5")
MAX_TENURE_MONTHS = 24


class Loan(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="loans",
        on_delete=models.CASCADE,
    )

    principal = models.DecimalField(max_digits=14, decimal_places=2)
    tenure_months = models.PositiveIntegerField(
        help_text="Repayment period in months (max 11)"
    )
    interest_rate = models.DecimalField(
        max_digits=6, decimal_places=4,
        default=MONTHLY_INTEREST_RATE,
        help_text="Monthly interest rate at time of application"
    )

    total_repayable = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    monthly_installment = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )

    status = models.CharField(
        max_length=20, choices=LoanStatus.choices, default=LoanStatus.PENDING
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="loans_approved",
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    disbursed_at = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Loan({self.uid}) - {self.user} - {self.status}"

    @staticmethod
    def calculate_summary(principal: Decimal, tenure_months: int) -> dict:
        rate = MONTHLY_INTEREST_RATE
        total_interest = principal * rate * tenure_months
        total_repayable = principal + total_interest
        monthly_installment = (total_repayable / tenure_months).quantize(Decimal("0.01"))
        return {
            "principal": principal,
            "tenure_months": tenure_months,
            "monthly_interest_rate": rate,
            "total_interest": total_interest.quantize(Decimal("0.01")),
            "total_repayable": total_repayable.quantize(Decimal("0.01")),
            "monthly_installment": monthly_installment,
        }


class LoanRepaymentSchedule(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    loan = models.ForeignKey(Loan, related_name="schedule", on_delete=models.CASCADE)

    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )

    is_paid = models.BooleanField(default=False)
    is_rolled_over = models.BooleanField(
        default=False, help_text="True if wallet had insufficient funds on due date"
    )
    extra_interest = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00"),
        help_text="Accumulated penalty interest from rollovers"
    )

    paid_at = models.DateTimeField(null=True, blank=True)
    wallet_transaction = models.OneToOneField(
        "wallet.WalletTransaction",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="repayment_schedule",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["installment_number"]
        unique_together = [("loan", "installment_number")]

    @property
    def total_amount_due(self):
        return self.amount_due + self.extra_interest

    def __str__(self):
        return f"Installment {self.installment_number} for Loan {self.loan.uid}"