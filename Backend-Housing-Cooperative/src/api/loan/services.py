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
    if schedule.is_paid:
        return

    if schedule.wallet_transaction_id:
        return
    
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