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
    """Create LoanRepaymentSchedule rows starting from next month."""
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
    """
    Approve + disburse:
    1. Compute totals
    2. Credit user wallet (LOAN_DISBURSEMENT)
    3. Generate schedule
    4. Mark loan ACTIVE
    """
    from api.wallet.models import Wallet

    summary = Loan.calculate_summary(loan.principal, loan.tenure_months)

    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=loan.user)

        # Credit wallet
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

        # Update loan
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
    Called by a scheduled task (e.g. Celery beat) on or after each due_date.
    - Deducts from wallet if balance is sufficient
    - If not, marks as rolled over and adds 0.5% penalty to next installment
    - If it's the last installment and still unpaid → DEFAULTED
    """
    if schedule.is_paid:
        return

    loan = schedule.loan
    wallet = Wallet.objects.select_for_update().get(user=loan.user)
    amount_owed = schedule.total_amount_due

    with db_transaction.atomic():
        if wallet.balance >= amount_owed:
            # Deduct
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

            # Check if all paid → complete the loan
            if not loan.schedule.filter(is_paid=False).exists():
                loan.status = LoanStatus.COMPLETED
                loan.save(update_fields=["status", "updated_at"])

        else:
            # Rollover: add 0.5% penalty on the outstanding amount
            penalty = (amount_owed * MONTHLY_INTEREST_RATE).quantize(Decimal("0.01"))
            schedule.is_rolled_over = True
            schedule.extra_interest += penalty
            schedule.save(update_fields=["is_rolled_over", "extra_interest", "updated_at"])

            # If this was the last installment, mark loan as defaulted
            if schedule.installment_number == loan.tenure_months:
                loan.status = LoanStatus.DEFAULTED
                loan.save(update_fields=["status", "updated_at"])