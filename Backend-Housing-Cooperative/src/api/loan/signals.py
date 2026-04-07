from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_q.models import Schedule
from django_q.tasks import schedule as q_schedule


@receiver(post_migrate)
def create_repayment_schedule(sender, **kwargs):
    """
    Runs after migrations → safe to access DB
    """

    if not Schedule.objects.filter(name="process_loan_repayments").exists():
        q_schedule(
            "api.loan.tasks.process_due_repayments",
            schedule_type=Schedule.DAILY,
            name="process_loan_repayments",
            repeats=-1,
        )