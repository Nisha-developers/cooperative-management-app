import uuid
from django.db import models


class ListingType(models.TextChoices):
    SALE = "sale", "For Sale"
    RENT = "rent", "For Rent"


class PropertyType(models.TextChoices):
    HOUSE = "house", "House"
    LAND = "land", "Land"


class ListingStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    PENDING = "pending", "Pending"
    SOLD = "sold", "Sold"
    RENTED = "rented", "Rented"


class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    listing_type = models.CharField(max_length=10, choices=ListingType.choices)
    property_type = models.CharField(max_length=10, choices=PropertyType.choices)
    status = models.CharField(
        max_length=20,
        choices=ListingStatus.choices,
        default=ListingStatus.AVAILABLE,
    )

    price = models.DecimalField(max_digits=14, decimal_places=2)

    # Sale-specific fields
    allows_installment = models.BooleanField(default=False)
    installment_duration_months = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Max duration allowed for installmental payment (months)"
    )
    minimum_initial_deposit = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True,
        help_text="Minimum deposit to initiate an installment purchase"
    )

    # Rent-specific fields
    rent_duration = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="e.g. per month, per year"
    )

    # Property details (land won't use bedrooms/bathrooms etc.)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    toilets = models.PositiveIntegerField(null=True, blank=True)
    area_sqm = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Total land/floor area in square metres"
    )
    is_furnished = models.BooleanField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()} - {self.get_property_type_display()})"