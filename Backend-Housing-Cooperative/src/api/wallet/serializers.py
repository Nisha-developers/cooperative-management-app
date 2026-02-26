from rest_framework import serializers
from .models import Wallet, WalletTransaction


class WalletTransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    confirmed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WalletTransaction
        fields = [
            "uid",
            "type",
            "source",
            "status",
            "amount",
            "reference",
            "created_by",
            "confirmed_by",
            "confirmed_at",
            "created_on",
            "updated_on",
        ]
        read_only_fields = [
            "uid",
            "reference",
            "status",
            "confirmed_by",
            "confirmed_at",
            "created_on",
            "updated_on",
        ]


class WalletSerializer(serializers.ModelSerializer):
    transactions = WalletTransactionSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = [
            "uid",
            "user",
            "balance",
            "transactions",
            "created_on",
            "updated_on",
        ]
        read_only_fields = [
            "uid",
            "balance",
            "created_on",
            "updated_on",
        ]


class WalletSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer without nested transactions — use this in list views or user profiles."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = [
            "uid",
            "user",
            "balance",
            "created_on",
            "updated_on",
        ]
        read_only_fields = fields