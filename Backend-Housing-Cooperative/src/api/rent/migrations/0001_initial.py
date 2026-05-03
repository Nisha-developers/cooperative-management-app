from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("listings", "0003_listingimage"),
        ("wallet", "0004_wallettransaction_rejection_reason_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Rent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("price_per_day", models.DecimalField(decimal_places=2, max_digits=14)),
                ("duration_days", models.PositiveIntegerField(help_text="Number of days the user wants to rent")),
                ("total_rent_cost", models.DecimalField(decimal_places=2, max_digits=14)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("status", models.CharField(
                    choices=[
                        ("PENDING", "Pending"), ("ACTIVE", "Active"),
                        ("COMPLETED", "Completed"), ("REJECTED", "Rejected"),
                        ("CANCELLED", "Cancelled"),
                    ],
                    default="PENDING", max_length=20,
                )),
                ("remark", models.TextField(blank=True, default="")),
                ("rejection_reason", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="rents_approved",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rents",
                        to="listings.listing",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wallet_transaction",
                    models.OneToOneField(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="rent",
                        to="wallet.wallettransaction",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
