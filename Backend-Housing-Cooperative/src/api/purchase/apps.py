from django.apps import AppConfig


class PurchaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.purchase"
    verbose_name = "Property Purchases"

    def ready(self):
        import api.purchase.signals  # noqa: F401 — connects post_migrate receiver