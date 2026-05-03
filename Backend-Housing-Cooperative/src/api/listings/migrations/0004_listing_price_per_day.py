from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0003_listingimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="rent_duration",
        ),
        migrations.AddField(
            model_name="listing",
            name="price_per_day",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Daily rental rate (price per day)",
                max_digits=14,
                null=True,
            ),
        ),
    ]
