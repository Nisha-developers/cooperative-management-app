from django.contrib import admin
from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title", "listing_type", "property_type",
        "status", "price", "allows_installment", "city", "state", "created_at"
    )
    list_filter = ("listing_type", "property_type", "status", "allows_installment", "state")
    search_fields = ("title", "address", "city", "state")
    readonly_fields = ("id", "created_at", "updated_at")