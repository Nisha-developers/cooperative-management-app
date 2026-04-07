from django.utils import timezone
from .models import LoanStatus, LoanRepaymentSchedule
from .services import process_repayment


def process_due_repayments():
    today = timezone.now().date()
    due_schedules = (
        LoanRepaymentSchedule.objects
        .select_related("loan__user__wallet")
        .filter(
            is_paid=False,
            due_date__lte=today,
            loan__status=LoanStatus.ACTIVE,
        )
        .order_by("loan", "installment_number")
    )
    for schedule in due_schedules:
        process_repayment(schedule)