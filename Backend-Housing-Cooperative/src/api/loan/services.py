from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import transaction as db_transaction
from django.utils import timezone

from api.wallet.models import (
    Wallet, WalletTransaction,
    WalletTransactionType, WalletTransactionSource, WalletTransactionStatus,
)
from .models import Loan, LoanRepaymentSchedule, LoanStatus, MONTHLY_INTEREST_RATE


def generate_repayment_schedule(loan: Loan):
    start_date = date.today() + relativedelta(months=1)
    schedules = []
    for i in range(1, loan.tenure_months + 1):
        schedules.append(LoanRepaymentSchedule(
            loan=loan,
            installment_number=i,
            due_date=start_date + relativedelta(months=i - 1),
            amount_due=loan.monthly_installment,
        ))
    LoanRepaymentSchedule.objects.bulk_create(schedules)


def disburse_loan(loan: Loan, admin_user):
    summary = Loan.calculate_summary(loan.principal, loan.tenure_months)

    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=loan.user)

        WalletTransaction.objects.create(
            wallet=wallet,
            type=WalletTransactionType.CREDIT,
            source=WalletTransactionSource.LOAN_DISBURSEMENT,
            status=WalletTransactionStatus.CONFIRMED,
            amount=loan.principal,
            remark=f"Loan disbursement — Loan #{loan.uid}",
            created_by=admin_user,
            confirmed_by=admin_user,
            confirmed_at=timezone.now(),
        )
        wallet.balance += loan.principal
        wallet.save(update_fields=["balance", "updated_on"])

        loan.total_repayable = summary["total_repayable"]
        loan.monthly_installment = summary["monthly_installment"]
        loan.status = LoanStatus.ACTIVE
        loan.approved_by = admin_user
        loan.approved_at = timezone.now()
        loan.disbursed_at = timezone.now()
        loan.save()

        generate_repayment_schedule(loan)


def process_repayment(schedule: LoanRepaymentSchedule):
    """
    Core repayment logic — used by both the scheduler and the manual repay endpoint.
    Returns a result dict so callers can surface feedback to the user.
    """
    if schedule.is_paid:
        return {"status": "already_paid", "message": "This installment is already paid."}

    if schedule.wallet_transaction_id:
        return {"status": "already_paid", "message": "This installment is already paid."}

    loan = schedule.loan

    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=loan.user)
        amount_owed = schedule.total_amount_due

        if wallet.balance >= amount_owed:
            tx = WalletTransaction.objects.create(
                wallet=wallet,
                type=WalletTransactionType.DEBIT,
                source=WalletTransactionSource.LOAN_REPAYMENT,
                status=WalletTransactionStatus.CONFIRMED,
                amount=amount_owed,
                remark=f"Loan repayment — installment {schedule.installment_number} of {loan.tenure_months}",
                confirmed_at=timezone.now(),
            )
            wallet.balance -= amount_owed
            wallet.save(update_fields=["balance", "updated_on"])

            schedule.amount_paid = amount_owed
            schedule.is_paid = True
            schedule.paid_at = timezone.now()
            schedule.wallet_transaction = tx
            schedule.save()

            # Mark loan completed if all installments paid
            if not loan.schedule.filter(is_paid=False).exists():
                loan.status = LoanStatus.COMPLETED
                loan.save(update_fields=["status", "updated_at"])
                return {
                    "status": "success",
                    "message": "Installment paid. Loan fully repaid — congratulations!",
                    "amount_deducted": str(amount_owed),
                    "loan_completed": True,
                }

            return {
                "status": "success",
                "message": f"Installment {schedule.installment_number} paid successfully.",
                "amount_deducted": str(amount_owed),
                "loan_completed": False,
            }

        else:
            # Insufficient balance — rollover with penalty
            penalty = (amount_owed * MONTHLY_INTEREST_RATE).quantize(Decimal("0.01"))
            schedule.is_rolled_over = True
            schedule.extra_interest += penalty
            schedule.save(update_fields=["is_rolled_over", "extra_interest", "updated_at"])

            # Last installment still unpaid → default
            if schedule.installment_number == loan.tenure_months:
                loan.status = LoanStatus.DEFAULTED
                loan.save(update_fields=["status", "updated_at"])

            return {
                "status": "insufficient_funds",
                "message": (
                    f"Insufficient wallet balance. ₦{amount_owed:,.2f} required, "
                    f"₦{wallet.balance:,.2f} available. "
                    f"A penalty of ₦{penalty:,.2f} has been added."
                ),
                "amount_required": str(amount_owed),
                "wallet_balance": str(wallet.balance),
                "penalty_added": str(penalty),
            }


def get_loan_balance_summary(loan: Loan) -> dict:
    """
    Returns total outstanding balance and this month's due amount for a loan.
    'This month' means the earliest unpaid installment whose due_date falls
    in the current calendar month, or the next upcoming unpaid installment
    if none falls this month.
    """
    today = timezone.now().date()
    unpaid = loan.schedule.filter(is_paid=False).order_by("installment_number")

    # Total outstanding = sum of total_amount_due across all unpaid installments
    total_outstanding = sum(s.total_amount_due for s in unpaid)

    # This month's installment: earliest unpaid due this month, else next upcoming
    this_month_schedule = (
        unpaid.filter(due_date__year=today.year, due_date__month=today.month).first()
        or unpaid.first()
    )

    this_month_due = this_month_schedule.total_amount_due if this_month_schedule else Decimal("0.00")
    this_month_due_date = this_month_schedule.due_date if this_month_schedule else None
    this_month_installment_number = this_month_schedule.installment_number if this_month_schedule else None

    return {
        "total_outstanding": total_outstanding.quantize(Decimal("0.01")),
        "this_month_due": this_month_due.quantize(Decimal("0.01")),
        "this_month_due_date": this_month_due_date,
        "this_month_installment_number": this_month_installment_number,
        "installments_remaining": unpaid.count(),
    }