from django.core.management.base import BaseCommand
from api.purchase.tasks import process_due_installments


class Command(BaseCommand):
    help = "Manually trigger processing of all due property installment payments."

    def handle(self, *args, **options):
        self.stdout.write("Processing due property installments...")
        process_due_installments()
        self.stdout.write(self.style.SUCCESS("Done."))