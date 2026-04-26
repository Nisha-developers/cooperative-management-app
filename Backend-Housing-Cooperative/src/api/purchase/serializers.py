from decimal import Decimal
from rest_framework import serializers
from django.utils import timezone

from api.listings.models import Listing, ListingType, ListingStatus, PropertyType
from .models import Purchase, PurchaseInstallmentSchedule, PurchaseStatus, PurchaseType


# ── Helpers ──────────────────────────────────────────────────────────────────

def get_listing_or_error(listing_id):
    try:
        return Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return None


# ── Preview ───────────────────────────────────────────────────────────────────

class PurchasePreviewSerializer(serializers.Serializer):
    listing_id = serializers.UUIDField()
    purchase_type = serializers.ChoiceField(choices=PurchaseType.choices)
    initial_deposit = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True
    )
    tenure_months = serializers.IntegerField(
        min_value=1, required=False, allow_null=True
    )

    def validate(self, data):
        listing = get_listing_or_error(data["listing_id"])
        if not listing:
            raise serializers.ValidationError({"listing_id": "Listing not found."})

        if listing.listing_type != ListingType.SALE:
            raise serializers.ValidationError(
                {"listing_id": "Only properties listed for sale can be purchased."}
            )

        if listing.status != ListingStatus.AVAILABLE:
            raise serializers.ValidationError(
                {"listing_id": f"This property is not available (status: {listing.status})."}
            )

        if data["purchase_type"] == PurchaseType.INSTALLMENT:
            if not listing.allows_installment:
                raise serializers.ValidationError(
                    {"purchase_type": "This property does not support installment payments."}
                )
            if not data.get("initial_deposit"):
                raise serializers.ValidationError(
                    {"initial_deposit": "Initial deposit is required for installment purchase."}
                )
            if not data.get("tenure_months"):
                raise serializers.ValidationError(
                    {"tenure_months": "Tenure in months is required for installment purchase."}
                )

            deposit = data["initial_deposit"]
            if deposit < listing.minimum_initial_deposit:
                raise serializers.ValidationError(
                    {
                        "initial_deposit": (
                            f"Minimum deposit is ₦{listing.minimum_initial_deposit:,.2f}."
                        )
                    }
                )

            if deposit >= listing.price:
                raise serializers.ValidationError(
                    {"initial_deposit": "Deposit cannot equal or exceed the full property price."}
                )

            if data["tenure_months"] > listing.installment_duration_months:
                raise serializers.ValidationError(
                    {
                        "tenure_months": (
                            f"Maximum installment duration for this property is "
                            f"{listing.installment_duration_months} months."
                        )
                    }
                )

        data["listing"] = listing
        return data


# ── Application ────────────────────────────────────────────────────────────────

class PurchaseApplicationSerializer(serializers.Serializer):
    listing_id = serializers.UUIDField()
    purchase_type = serializers.ChoiceField(choices=PurchaseType.choices)
    initial_deposit = serializers.DecimalField(
        max_digits=14, decimal_places=2, required=False, allow_null=True
    )
    tenure_months = serializers.IntegerField(
        min_value=1, required=False, allow_null=True
    )

    def validate(self, data):
        user = self.context["request"].user
        listing = get_listing_or_error(data["listing_id"])

        if not listing:
            raise serializers.ValidationError({"listing_id": "Listing not found."})

        if listing.listing_type != ListingType.SALE:
            raise serializers.ValidationError(
                {"listing_id": "Only properties listed for sale can be purchased."}
            )

        if listing.status != ListingStatus.AVAILABLE:
            raise serializers.ValidationError(
                {"listing_id": f"This property is not available (status: {listing.status})."}
            )

        # Prevent duplicate open purchase on the same listing by the same user
        if Purchase.objects.filter(
            user=user,
            listing=listing,
            status__in=[PurchaseStatus.PENDING, PurchaseStatus.ACTIVE],
        ).exists():
            raise serializers.ValidationError(
                "You already have an open purchase application for this property."
            )

        if data["purchase_type"] == PurchaseType.INSTALLMENT:
            if not listing.allows_installment:
                raise serializers.ValidationError(
                    {"purchase_type": "This property does not support installment payments."}
                )
            if not data.get("initial_deposit"):
                raise serializers.ValidationError(
                    {"initial_deposit": "Initial deposit is required for installment purchase."}
                )
            if not data.get("tenure_months"):
                raise serializers.ValidationError(
                    {"tenure_months": "Tenure in months is required for installment purchase."}
                )

            deposit = data["initial_deposit"]
            if deposit < listing.minimum_initial_deposit:
                raise serializers.ValidationError(
                    {
                        "initial_deposit": (
                            f"Minimum deposit is ₦{listing.minimum_initial_deposit:,.2f}."
                        )
                    }
                )

            if deposit >= listing.price:
                raise serializers.ValidationError(
                    {"initial_deposit": "Deposit cannot equal or exceed the full property price."}
                )

            if data["tenure_months"] > listing.installment_duration_months:
                raise serializers.ValidationError(
                    {
                        "tenure_months": (
                            f"Maximum installment duration for this property is "
                            f"{listing.installment_duration_months} months."
                        )
                    }
                )

            # Wallet balance check: must cover at least the deposit
            try:
                balance = user.wallet.balance
            except Exception:
                balance = Decimal("0.00")

            if balance < deposit:
                raise serializers.ValidationError(
                    {
                        "initial_deposit": (
                            f"Insufficient wallet balance. "
                            f"₦{deposit:,.2f} required, ₦{balance:,.2f} available."
                        )
                    }
                )

        elif data["purchase_type"] == PurchaseType.OUTRIGHT:
            # Wallet must cover the full price for outright
            try:
                balance = user.wallet.balance
            except Exception:
                balance = Decimal("0.00")

            if balance < listing.price:
                raise serializers.ValidationError(
                    {
                        "purchase_type": (
                            f"Insufficient wallet balance for outright purchase. "
                            f"₦{listing.price:,.2f} required, ₦{balance:,.2f} available."
                        )
                    }
                )

        data["listing"] = listing
        return data


# ── Schedule ──────────────────────────────────────────────────────────────────

class InstallmentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInstallmentSchedule
        fields = [
            "uid",
            "installment_number",
            "due_date",
            "amount_due",
            "amount_paid",
            "is_paid",
            "is_overdue",
            "paid_at",
        ]


# ── Balance summary ────────────────────────────────────────────────────────────

class PurchaseBalanceSummarySerializer(serializers.Serializer):
    total_outstanding = serializers.DecimalField(max_digits=14, decimal_places=2)
    this_month_due = serializers.DecimalField(max_digits=14, decimal_places=2)
    this_month_due_date = serializers.DateField(allow_null=True)
    this_month_installment_number = serializers.IntegerField(allow_null=True)
    installments_remaining = serializers.IntegerField()


# ── Detail / List ──────────────────────────────────────────────────────────────

class PurchaseDetailSerializer(serializers.ModelSerializer):
    schedule = InstallmentScheduleSerializer(many=True, read_only=True)
    balance_summary = serializers.SerializerMethodField()
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    listing_address = serializers.CharField(source="listing.address", read_only=True)
    property_type = serializers.CharField(source="listing.property_type", read_only=True)

    class Meta:
        model = Purchase
        fields = [
            "uid",
            "listing_title",
            "listing_address",
            "property_type",
            "purchase_type",
            "property_price",
            "initial_deposit",
            "balance_after_deposit",
            "tenure_months",
            "monthly_installment",
            "total_repayable",
            "status",
            "approved_at",
            "remark",
            "created_at",
            "balance_summary",
            "schedule",
        ]

    def get_balance_summary(self, obj):
        if obj.status != "ACTIVE" or obj.purchase_type != PurchaseType.INSTALLMENT:
            return None
        from .services import get_purchase_balance_summary
        data = get_purchase_balance_summary(obj)
        return PurchaseBalanceSummarySerializer(data).data


class PurchaseListSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    property_type = serializers.CharField(source="listing.property_type", read_only=True)

    class Meta:
        model = Purchase
        fields = [
            "uid",
            "listing_title",
            "property_type",
            "purchase_type",
            "property_price",
            "initial_deposit",
            "monthly_installment",
            "status",
            "created_at",
        ]


# ── Admin serializers ──────────────────────────────────────────────────────────

class AdminPurchaseDetailSerializer(serializers.ModelSerializer):
    schedule = InstallmentScheduleSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_membership = serializers.CharField(source="user.membership_id", read_only=True)
    listing_title = serializers.CharField(source="listing.title", read_only=True)
    listing_address = serializers.CharField(source="listing.address", read_only=True)
    property_type = serializers.CharField(source="listing.property_type", read_only=True)
    balance_summary = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            "uid",
            "user_email",
            "user_membership",
            "listing_title",
            "listing_address",
            "property_type",
            "purchase_type",
            "property_price",
            "initial_deposit",
            "balance_after_deposit",
            "tenure_months",
            "monthly_installment",
            "total_repayable",
            "status",
            "remark",
            "approved_at",
            "created_at",
            "balance_summary",
            "schedule",
        ]

    def get_balance_summary(self, obj):
        if obj.status != "ACTIVE" or obj.purchase_type != PurchaseType.INSTALLMENT:
            return None
        from .services import get_purchase_balance_summary
        data = get_purchase_balance_summary(obj)
        return PurchaseBalanceSummarySerializer(data).data