from django.contrib import admin
from .models import Purchase, PurchaseInstallmentSchedule


class PurchaseInstallmentInline(admin.TabularInline):
    model = PurchaseInstallmentSchedule
    extra = 0
    readonly_fields = (
        "uid", "installment_number", "due_date",
        "amount_due", "amount_paid", "is_paid", "is_overdue", "paid_at",
    )
    can_delete = False


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "uid", "user", "listing", "purchase_type",
        "property_price", "status", "created_at",
    )
    list_filter = ("status", "purchase_type")
    search_fields = ("uid", "user__email", "listing__title")
    readonly_fields = (
        "uid", "user", "listing", "purchase_type", "property_price",
        "initial_deposit", "balance_after_deposit", "tenure_months",
        "monthly_installment", "total_repayable",
        "approved_by", "approved_at", "created_at", "updated_at",
    )
    inlines = [PurchaseInstallmentInline]


@admin.register(PurchaseInstallmentSchedule)
class PurchaseInstallmentScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "uid", "purchase", "installment_number",
        "due_date", "amount_due", "is_paid", "is_overdue",
    )
    list_filter = ("is_paid", "is_overdue")
    search_fields = ("purchase__uid", "purchase__user__email")
    readonly_fields = (
        "uid", "purchase", "installment_number", "due_date",
        "amount_due", "amount_paid", "is_paid", "is_overdue",
        "paid_at", "wallet_transaction", "created_at", "updated_at",
    )