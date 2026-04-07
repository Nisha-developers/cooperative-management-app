from decimal import Decimal
from rest_framework import serializers
from django.utils import timezone
from .models import Loan, LoanRepaymentSchedule, MAX_TENURE_MONTHS

LOAN_MIN_BALANCE = 500_000
LOAN_MIN_MEMBERSHIP_MONTHS = 6


def check_loan_eligibility(user):
    """Returns (is_eligible, reason, max_loan_amount)"""
    try:
        balance = user.wallet.balance
    except Exception:
        balance = Decimal("0.00")

    months_since_joined = (timezone.now() - user.created_at).days // 30
    has_enough_balance = balance >= LOAN_MIN_BALANCE
    has_tenure = months_since_joined >= LOAN_MIN_MEMBERSHIP_MONTHS
    is_eligible = has_enough_balance or has_tenure
    max_loan_amount = balance * 2 if is_eligible else Decimal("0.00")

    reason = None
    if not is_eligible:
        reason = "Minimum 6 months membership or ₦500,000 balance required"

    return is_eligible, reason, max_loan_amount


class LoanPreviewSerializer(serializers.Serializer):
    principal = serializers.DecimalField(max_digits=14, decimal_places=2)
    tenure_months = serializers.IntegerField(min_value=1, max_value=MAX_TENURE_MONTHS)

    def validate_principal(self, value):
        if value <= 0:
            raise serializers.ValidationError("Principal must be greater than zero.")
        return value


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["uid", "principal", "tenure_months", "status", "created_at"]
        read_only_fields = ["uid", "status", "created_at"]

    def validate_tenure_months(self, value):
        if value > MAX_TENURE_MONTHS:
            raise serializers.ValidationError(
                f"Maximum tenure is {MAX_TENURE_MONTHS} months."
            )
        return value

    def validate(self, data):
        user = self.context["request"].user
        principal = data.get("principal")

        # 1. Check eligibility gate first
        is_eligible, reason, max_loan_amount = check_loan_eligibility(user)
        if not is_eligible:
            raise serializers.ValidationError({"eligibility": reason})

        # 2. Check for existing active/pending loan
        if Loan.objects.filter(user=user, status__in=["PENDING", "ACTIVE"]).exists():
            raise serializers.ValidationError(
                "You already have an active or pending loan. Repay it before applying again."
            )

        # 3. Check principal against max allowed (2x balance)
        if principal > max_loan_amount:
            raise serializers.ValidationError(
                {"principal": f"Maximum loan amount is ₦{max_loan_amount:,.2f} (2× your balance)."}
            )

        return data


class RepaymentScheduleSerializer(serializers.ModelSerializer):
    total_amount_due = serializers.DecimalField(
        max_digits=14, decimal_places=2, read_only=True
    )

    class Meta:
        model = LoanRepaymentSchedule
        fields = [
            "uid", "installment_number", "due_date",
            "amount_due", "extra_interest", "total_amount_due",
            "amount_paid", "is_paid", "is_rolled_over", "paid_at",
        ]


class LoanDetailSerializer(serializers.ModelSerializer):
    schedule = RepaymentScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = [
            "uid", "principal", "tenure_months", "interest_rate",
            "total_repayable", "monthly_installment", "status",
            "approved_at", "disbursed_at", "remark", "created_at", "schedule",
        ]


class LoanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "uid", "principal", "tenure_months",
            "total_repayable", "monthly_installment",
            "status", "created_at",
        ]


class AdminLoanDetailSerializer(serializers.ModelSerializer):
    schedule = RepaymentScheduleSerializer(many=True, read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_membership = serializers.CharField(source="user.membership_id", read_only=True)

    class Meta:
        model = Loan
        fields = [
            "uid", "user_email", "user_membership",
            "principal", "tenure_months", "interest_rate",
            "total_repayable", "monthly_installment", "status",
            "remark", "approved_at", "disbursed_at", "created_at", "schedule",
        ]