from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.wallet.models import Wallet
from api.wallet.serializers import WalletSummarySerializer
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import User, UserProfile
from django.utils import timezone

LOAN_MIN_BALANCE = 500_000
LOAN_MIN_MEMBERSHIP_MONTHS = 6


def get_loan_eligibility(user):
    """Returns eligibility dict for a user."""
    try:
        wallet = user.wallet
        balance = wallet.balance
    except ObjectDoesNotExist:
        balance = 0

    has_enough_balance = balance >= LOAN_MIN_BALANCE

    joined_at = user.created_at
    months_since_joined = (timezone.now() - joined_at).days // 30
    has_tenure = months_since_joined >= LOAN_MIN_MEMBERSHIP_MONTHS

    is_eligible = has_enough_balance or has_tenure
    max_loan_amount = balance * 2 if is_eligible else 0

    return {
        "is_eligible": is_eligible,
        "reason": (
            "Eligible based on balance and/or tenure"
            if is_eligible
            else "Minimum 6 months membership or ₦500,000 balance required"
        ),
        "max_loan_amount": str(max_loan_amount),
        "months_since_joined": months_since_joined,
    }


def get_active_loan_summary(user):
    """
    Returns a compact loan summary if the user has an ACTIVE loan, else None.
    Pulls total_outstanding and this_month_due from the shared service function
    so the logic is never duplicated.
    """
    try:
        loan = user.loans.filter(status="ACTIVE").select_related(None).prefetch_related("schedule").first()
    except Exception:
        return None

    if not loan:
        return None

    from api.loan.services import get_loan_balance_summary
    summary = get_loan_balance_summary(loan)

    return {
        "loan_uid": str(loan.uid),
        "principal": str(loan.principal),
        "total_repayable": str(loan.total_repayable),
        "monthly_installment": str(loan.monthly_installment),
        "tenure_months": loan.tenure_months,
        "disbursed_at": loan.disbursed_at,
        # balance fields
        "total_outstanding": str(summary["total_outstanding"]),
        "this_month_due": str(summary["this_month_due"]),
        "this_month_due_date": str(summary["this_month_due_date"]) if summary["this_month_due_date"] else None,
        "this_month_installment_number": summary["this_month_installment_number"],
        "installments_remaining": summary["installments_remaining"],
    }


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'gender', 'full_name', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        is_admin = validated_data.pop('is_admin', False)
        user = User.objects.create_user(
            **validated_data,
            is_active=False
        )
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        try:
            wallet = user.wallet
        except ObjectDoesNotExist:
            wallet = None

        wallet_data = WalletSummarySerializer(wallet).data if wallet else None

        data.update({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
                "membership_id": user.membership_id
            },
            "wallet": wallet_data,
            "loan_eligibility": get_loan_eligibility(user),
            "active_loan": get_active_loan_summary(user),  # null if no active loan
        })

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'full_name', 'phone_number', 'account_number', 'account_name', 'bank_name', 'address', 'updated_at']
        read_only_fields = ['id', 'email', 'full_name', 'updated_at']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "membership_id",
            "is_active",
        ]


class AdminUserDetailSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "is_admin",
            "membership_id",
            "wallet",
        ]

    def get_wallet(self, obj):
        try:
            wallet = obj.wallet
            return WalletSummarySerializer(wallet).data
        except ObjectDoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        wallet_data = representation.pop("wallet")
        return {
            "user": representation,
            "wallet": wallet_data,
        }