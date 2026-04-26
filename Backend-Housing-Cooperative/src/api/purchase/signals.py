from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_q.models import Schedule
from django_q.tasks import schedule as q_schedule


@receiver(post_migrate)
def create_purchase_installment_schedule(sender, **kwargs):
    """
    Runs after every migration — creates the daily installment processing
    schedule if it doesn't already exist.
    Mirrors api.loan.signals.create_repayment_schedule.
    """
    if not Schedule.objects.filter(name="process_purchase_installments").exists():
        q_schedule(
            "api.purchase.tasks.process_due_installments",
            schedule_type=Schedule.DAILY,
            name="process_purchase_installments",
            repeats=-1,
        )