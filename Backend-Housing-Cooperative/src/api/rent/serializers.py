from decimal import Decimal
from rest_framework import serializers

from api.listings.models import Listing, ListingType, ListingStatus
from .models import Rent, RentStatus


def get_listing_or_error(listing_id):
    try:
        return Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return None


class RentPreviewSerializer(serializers.Serializer):
    listing_id = serializers.UUIDField()
    duration_days = serializers.IntegerField(min_value=1)

    def validate(self, data):
        listing = get_listing_or_error(data["listing_id"])
        if not listing:
            raise serializers.ValidationError({"listing_id": "Listing not found."})

        if listing.listing_type != ListingType.RENT:
            raise serializers.ValidationError(
                {"listing_id": "This property is not listed for rent."}
            )

        if listing.status != ListingStatus.AVAILABLE:
            raise serializers.ValidationError(
                {"listing_id": f"This property is not available (status: {listing.status})."}
            )

        if not listing.price_per_day:
            raise serializers.ValidationError(
                {"listing_id": "This listing does not have a daily rate configured."}
            )

        data["listing"] = listing
        return data


class RentApplicationSerializer(serializers.Serializer):
    listing_id = serializers.UUIDField()
    duration_days = serializers.IntegerField(min_value=1)

    def validate(self, data):
        user = self.context["request"].user
        listing = get_listing_or_error(data["listing_id"])

        if not listing:
            raise serializers.ValidationError({"listing_id": "Listing not found."})

        if listing.listing_type != ListingType.RENT:
            raise serializers.ValidationError(
                {"listing_id": "This property is not listed for rent."}
            )

        if listing.status != ListingStatus.AVAILABLE:
            raise serializers.ValidationError(
                {"listing_id": f"This property is not available (status: {listing.status})."}
            )

        if not listing.price_per_day:
            raise serializers.ValidationError(
                {"listing_id": "This listing does not have a daily rate configured."}
            )

        # Prevent duplicate open rent on the same listing
        if Rent.objects.filter(
            user=user,
            listing=listing,
            status__in=[RentStatus.PENDING, RentStatus.ACTIVE],
        ).exists():
            raise serializers.ValidationError(
                "You already have an open rent application for this property."
            )

        total_cost = Rent.calculate_total(listing.price_per_day, data["duration_days"])

        # Check wallet balance covers total rent cost
        try:
            balance = user.wallet.balance
        except Exception:
            balance = Decimal("0.00")

        if balance < total_cost:
            raise serializers.ValidationError(
                {
                    "duration_days": (
                        f"Insufficient wallet balance. "
                        f"₦{total_cost:,.2f} required for {data['duration_days']} days, "
                        f"₦{balance:,.2f} available."
                    )
                }
            )

        data["listing"] = listing
        data["total_cost"] = total_cost
        return data


class RentDetailSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    listing_address = serializers.CharField(source="listing.address", read_only=True)
    property_type = serializers.CharField(source="listing.property_type", read_only=True)

    class Meta:
        model = Rent
        fields = [
            "uid",
            "listing_title",
            "listing_address",
            "property_type",
            "price_per_day",
            "duration_days",
            "total_rent_cost",
            "start_date",
            "end_date",
            "status",
            "remark",
            "rejection_reason",
            "approved_at",
            "created_at",
        ]


class RentListSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    property_type = serializers.CharField(source="listing.property_type", read_only=True)

    class Meta:
        model = Rent
        fields = [
            "uid",
            "listing_title",
            "property_type",
            "price_per_day",
            "duration_days",
            "total_rent_cost",
            "start_date",
            "end_date",
            "status",
            "created_at",
        ]


class AdminRentDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_membership = serializers.CharField(source="user.membership_id", read_only=True)
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    listing_address = serializers.CharField(source="listing.address", read_only=True)
    property_type = serializers.CharField(source="listing.property_type", read_only=True)

    class Meta:
        model = Rent
        fields = [
            "uid",
            "user_email",
            "user_membership",
            "listing_title",
            "listing_address",
            "property_type",
            "price_per_day",
            "duration_days",
            "total_rent_cost",
            "start_date",
            "end_date",
            "status",
            "remark",
            "rejection_reason",
            "approved_by",
            "approved_at",
            "created_at",
        ]
