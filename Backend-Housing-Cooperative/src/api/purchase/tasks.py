from django.utils import timezone

from .models import PurchaseStatus, PurchaseInstallmentSchedule
from .services import process_installment_payment


def process_due_installments():
    """
    Daily task: process all installment payments whose due_date has passed
    and that have not yet been paid.

    Mirrors api.loan.tasks.process_due_repayments — registered via signals.py.
    """
    today = timezone.now().date()
    due_schedules = (
        PurchaseInstallmentSchedule.objects
        .select_related("purchase__user__wallet", "purchase__listing")
        .filter(
            is_paid=False,
            due_date__lte=today,
            purchase__status=PurchaseStatus.ACTIVE,
        )
        .order_by("purchase", "installment_number")
    )
    for schedule in due_schedules:
        process_installment_payment(schedule)