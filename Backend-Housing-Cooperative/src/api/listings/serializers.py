from rest_framework import serializers
from .models import Listing, ListingType, PropertyType


class ListingSerializer(serializers.ModelSerializer):
    """Full serializer — used for create, retrieve, update."""

    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, data):
        # On partial updates, fall back to the existing instance values
        listing_type = data.get("listing_type", getattr(self.instance, "listing_type", None))
        property_type = data.get("property_type", getattr(self.instance, "property_type", None))
        allows_installment = data.get(
            "allows_installment",
            getattr(self.instance, "allows_installment", False)
        )

        # Land cannot be rented
        if property_type == PropertyType.LAND and listing_type == ListingType.RENT:
            raise serializers.ValidationError(
                {"property_type": "Land cannot be listed for rent."}
            )

        # Installment only applies to sale
        if listing_type == ListingType.RENT and allows_installment:
            raise serializers.ValidationError(
                {"allows_installment": "Rental listings cannot have installment payments."}
            )

        # If installment is enabled, require supporting fields
        if allows_installment:
            if not data.get("installment_duration_months"):
                raise serializers.ValidationError(
                    {"installment_duration_months": "Required when installment is allowed."}
                )
            if not data.get("minimum_initial_deposit"):
                raise serializers.ValidationError(
                    {"minimum_initial_deposit": "Required when installment is allowed."}
                )

        # Rent duration required for rental listings
        if listing_type == ListingType.RENT and not data.get("rent_duration"):
            raise serializers.ValidationError(
                {"rent_duration": "Rent duration is required for rental listings (in months)."}
            )

        return data


class ListingListSerializer(serializers.ModelSerializer):
    """Lighter serializer for the list endpoint — no heavy/unused fields."""

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "listing_type",
            "property_type",
            "status",
            "price",
            "allows_installment",
            "state",
            "city",
            "bedrooms",
            "bathrooms",
            "area_sqm",
            "created_at",
        )
