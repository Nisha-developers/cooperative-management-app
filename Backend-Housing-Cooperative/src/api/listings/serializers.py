from rest_framework import serializers
from .models import Listing, ListingImage, ListingType, PropertyType


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["uid", "image_url", "uploaded_at"]


class ListingImageUploadSerializer(serializers.Serializer):
    """Accepts a raw image file for upload to Cloudinary."""
    image = serializers.ImageField()


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, data):
        listing_type = data.get("listing_type", getattr(self.instance, "listing_type", None))
        property_type = data.get("property_type", getattr(self.instance, "property_type", None))
        allows_installment = data.get(
            "allows_installment",
            getattr(self.instance, "allows_installment", False)
        )

        if property_type == PropertyType.LAND and listing_type == ListingType.RENT:
            raise serializers.ValidationError(
                {"property_type": "Land cannot be listed for rent."}
            )

        if listing_type == ListingType.RENT and allows_installment:
            raise serializers.ValidationError(
                {"allows_installment": "Rental listings cannot have installment payments."}
            )

        if allows_installment:
            if not data.get("installment_duration_months"):
                raise serializers.ValidationError(
                    {"installment_duration_months": "Required when installment is allowed."}
                )
            if not data.get("minimum_initial_deposit"):
                raise serializers.ValidationError(
                    {"minimum_initial_deposit": "Required when installment is allowed."}
                )

        if listing_type == ListingType.RENT:
            price_per_day = data.get("price_per_day")
            if not price_per_day:
                raise serializers.ValidationError(
                    {"price_per_day": "A daily rate is required for rental listings."}
                )

            # AUTO MIRROR PRICE
            data["price"] = price_per_day

        return data


class ListingListSerializer(serializers.ModelSerializer):
    """Lighter serializer for the list endpoint."""
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = (
            "id",
            "title",
            "listing_type",
            "property_type",
            "status",
            "price",
            "price_per_day",
            "allows_installment",
            "state",
            "city",
            "bedrooms",
            "bathrooms",
            "area_sqm",
            "images",
            "created_at",
        )