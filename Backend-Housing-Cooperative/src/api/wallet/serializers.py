from rest_framework import serializers

from .models import (
    Wallet,
    WalletPaymentProof,
    WalletTransaction,
    WalletTransactionSource,
    WalletTransactionType,
)


class WalletPaymentProofSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
 
    class Meta:
        model = WalletPaymentProof
        fields = ["uid", "image_url", "uploaded_by", "created_on", "updated_on"]
        read_only_fields = ["uid", "uploaded_by", "created_on", "updated_on"]

class WalletTransactionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    confirmed_by = serializers.StringRelatedField(read_only=True)
    payment_proof = WalletPaymentProofSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = WalletTransaction
        fields = [
            "uid",
            "type",
            "source",
            "status",
            "amount",
            "remark",
            "rejection_reason",
            "reference",
            "full_name",
            "payment_proof",
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
            "rejection_reason",
            "full_name",
            "payment_proof",
            "confirmed_by",
            "confirmed_at",
            "created_on",
            "updated_on",
        ]
        
    def get_full_name(self, obj):
        if obj.created_by:
            return obj.created_by.full_name
        return None


class CreditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ["uid", "source", "amount", "remark", "reference", "status", "created_on"]
        read_only_fields = ["uid", "reference", "status", "created_on"]

    def validate_source(self, value):
        allowed = {WalletTransactionSource.USER_TOPUP, WalletTransactionSource.TRANSFER}
        if value not in allowed:
            raise serializers.ValidationError(
                f"Invalid source for a credit. Allowed: {', '.join(allowed)}"
            )
        return value

    def create(self, validated_data):
        validated_data["type"] = WalletTransactionType.CREDIT
        validated_data["wallet"] = self.context["wallet"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class DebitTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ["uid", "source", "amount", "remark", "reference", "status", "created_on"]
        read_only_fields = ["uid", "reference", "status", "created_on"]

    def validate_source(self, value):
        allowed = {
            WalletTransactionSource.WITHDRAWAL,
            WalletTransactionSource.TRANSFER,
            WalletTransactionSource.PURCHASE,
        }
        if value not in allowed:
            raise serializers.ValidationError(
                f"Invalid source for a debit. Allowed: {', '.join(allowed)}"
            )
        return value

    def validate(self, attrs):
        wallet = self.context["wallet"]
        if wallet.balance < attrs.get("amount", 0):
            raise serializers.ValidationError({"amount": "Insufficient wallet balance."})
        return attrs

    def create(self, validated_data):
        validated_data["type"] = WalletTransactionType.DEBIT
        validated_data["wallet"] = self.context["wallet"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class TransactionReviewSerializer(serializers.Serializer):
    remark = serializers.CharField(required=False, allow_blank=True, default="")


class TransactionRejectSerializer(serializers.Serializer):
    rejection_reason = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "A rejection reason is required.",
            "blank": "Rejection reason may not be blank.",
        }
    )

class ClientProofUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class AdminProofUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()


class WalletSerializer(serializers.ModelSerializer):
    transactions = WalletTransactionSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = ["uid", "user", "balance", "transactions", "created_on", "updated_on"]
        read_only_fields = ["uid", "balance", "created_on", "updated_on"]


class WalletSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["uid", "balance", "created_on", "updated_on"]
        read_only_fields = fields
