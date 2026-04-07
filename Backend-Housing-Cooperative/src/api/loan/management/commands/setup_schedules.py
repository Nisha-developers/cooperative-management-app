from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule as q_schedule


class Command(BaseCommand):
    help = "Create Django Q schedules"

    def handle(self, *args, **kwargs):
        if not Schedule.objects.filter(name="process_loan_repayments").exists():
            q_schedule(
                "api.loan.tasks.process_due_repayments",
                schedule_type=Schedule.MINUTES,
                minutes=5,
                name="process_loan_repayments",
                repeats=-1,
            )
            self.stdout.write(self.style.SUCCESS("Schedule created"))
        else:
            self.stdout.write("Schedule already exists")