from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import transaction as db_transaction
from django.utils import timezone

from api.wallet.models import (
    Wallet,
    WalletTransaction,
    WalletTransactionType,
    WalletTransactionSource,
    WalletTransactionStatus,
)
from api.listings.models import ListingStatus

from .models import (
    Purchase,
    PurchaseInstallmentSchedule,
    PurchaseStatus,
    PurchaseType,
)


# ── Schedule generation ────────────────────────────────────────────────────────

def generate_installment_schedule(purchase: Purchase):
    """Create monthly installment rows starting one month from today."""
    start_date = date.today() + relativedelta(months=1)
    schedules = [
        PurchaseInstallmentSchedule(
            purchase=purchase,
            installment_number=i,
            due_date=start_date + relativedelta(months=i - 1),
            amount_due=purchase.monthly_installment,
        )
        for i in range(1, purchase.tenure_months + 1)
    ]
    PurchaseInstallmentSchedule.objects.bulk_create(schedules)


# ── Approve / activate ─────────────────────────────────────────────────────────

def approve_purchase(purchase: Purchase, admin_user):
    """
    Admin approval flow:

    OUTRIGHT
    --------
    Debit full price from the buyer's wallet in one shot, mark listing SOLD,
    mark purchase COMPLETED immediately (no schedule needed).

    INSTALLMENT
    -----------
    1. Debit the initial deposit from the buyer's wallet.
    2. Generate the monthly installment schedule for the balance.
    3. Mark listing PENDING (reserved — not yet SOLD).
    4. Mark purchase ACTIVE.
    """
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=purchase.user)
        listing = purchase.listing

        if purchase.purchase_type == PurchaseType.OUTRIGHT:
            # ── Outright: single full-price debit ────────────────────────────
            tx = WalletTransaction.objects.create(
                wallet=wallet,
                type=WalletTransactionType.DEBIT,
                source=WalletTransactionSource.PURCHASE,
                status=WalletTransactionStatus.CONFIRMED,
                amount=purchase.property_price,
                remark=f"Outright purchase — {listing.title} (Purchase #{purchase.uid})",
                created_by=admin_user,
                confirmed_by=admin_user,
                confirmed_at=timezone.now(),
            )
            wallet.balance -= purchase.property_price
            wallet.save(update_fields=["balance", "updated_on"])

            listing.status = ListingStatus.SOLD
            listing.save(update_fields=["status", "updated_at"])

            purchase.status = PurchaseStatus.COMPLETED
            purchase.approved_by = admin_user
            purchase.approved_at = timezone.now()
            purchase.save()

        else:
            # ── Installment: debit deposit, schedule the rest ────────────────
            summary = Purchase.calculate_installment_summary(
                purchase.property_price,
                purchase.initial_deposit,
                purchase.tenure_months,
            )

            WalletTransaction.objects.create(
                wallet=wallet,
                type=WalletTransactionType.DEBIT,
                source=WalletTransactionSource.PURCHASE,
                status=WalletTransactionStatus.CONFIRMED,
                amount=purchase.initial_deposit,
                remark=(
                    f"Initial deposit — {listing.title} (Purchase #{purchase.uid})"
                ),
                created_by=admin_user,
                confirmed_by=admin_user,
                confirmed_at=timezone.now(),
            )
            wallet.balance -= purchase.initial_deposit
            wallet.save(update_fields=["balance", "updated_on"])

            # Persist computed financial fields
            purchase.balance_after_deposit = summary["balance_after_deposit"]
            purchase.monthly_installment = summary["monthly_installment"]
            purchase.total_repayable = summary["total_repayable"]
            purchase.status = PurchaseStatus.ACTIVE
            purchase.approved_by = admin_user
            purchase.approved_at = timezone.now()
            purchase.save()

            listing.status = ListingStatus.PENDING   # reserved
            listing.save(update_fields=["status", "updated_at"])

            generate_installment_schedule(purchase)


# ── Installment payment ────────────────────────────────────────────────────────

def process_installment_payment(schedule: PurchaseInstallmentSchedule) -> dict:
    """
    Core installment payment logic — called by both the manual pay endpoint
    and the daily scheduler.

    Returns a result dict that views / tasks can surface to the caller.
    """
    if schedule.is_paid:
        return {"status": "already_paid", "message": "This installment is already paid."}

    if schedule.wallet_transaction_id:
        return {"status": "already_paid", "message": "This installment is already paid."}

    purchase = schedule.purchase

    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=purchase.user)
        amount_due = schedule.amount_due

        if wallet.balance >= amount_due:
            tx = WalletTransaction.objects.create(
                wallet=wallet,
                type=WalletTransactionType.DEBIT,
                source=WalletTransactionSource.PURCHASE,
                status=WalletTransactionStatus.CONFIRMED,
                amount=amount_due,
                remark=(
                    f"Property installment payment — "
                    f"installment {schedule.installment_number} of {purchase.tenure_months} "
                    f"({purchase.listing.title})"
                ),
                confirmed_at=timezone.now(),
            )
            wallet.balance -= amount_due
            wallet.save(update_fields=["balance", "updated_on"])

            schedule.amount_paid = amount_due
            schedule.is_paid = True
            schedule.paid_at = timezone.now()
            schedule.wallet_transaction = tx
            schedule.save()

            # Check if all installments are now settled
            all_paid = not purchase.schedule.filter(is_paid=False).exists()
            if all_paid:
                purchase.status = PurchaseStatus.COMPLETED
                purchase.save(update_fields=["status", "updated_at"])

                # Mark the property SOLD now that full payment is complete
                purchase.listing.status = ListingStatus.SOLD
                purchase.listing.save(update_fields=["status", "updated_at"])

                return {
                    "status": "success",
                    "message": (
                        "Installment paid. All installments cleared — "
                        "congratulations on your new property!"
                    ),
                    "amount_deducted": str(amount_due),
                    "purchase_completed": True,
                }

            return {
                "status": "success",
                "message": (
                    f"Installment {schedule.installment_number} paid successfully."
                ),
                "amount_deducted": str(amount_due),
                "purchase_completed": False,
            }

        else:
            # Insufficient funds — flag as overdue, no penalty (property purchase ≠ loan)
            schedule.is_overdue = True
            schedule.save(update_fields=["is_overdue", "updated_at"])

            return {
                "status": "insufficient_funds",
                "message": (
                    f"Insufficient wallet balance. ₦{amount_due:,.2f} required, "
                    f"₦{wallet.balance:,.2f} available. "
                    f"Please fund your wallet before the next due date."
                ),
                "amount_required": str(amount_due),
                "wallet_balance": str(wallet.balance),
            }


# ── Balance summary ────────────────────────────────────────────────────────────

def get_purchase_balance_summary(purchase: Purchase) -> dict:
    """
    Returns the outstanding balance and the current month's due installment
    for an ACTIVE installment purchase.
    """
    today = timezone.now().date()
    unpaid = purchase.schedule.filter(is_paid=False).order_by("installment_number")

    total_outstanding = sum(s.amount_due for s in unpaid)

    this_month_schedule = (
        unpaid.filter(due_date__year=today.year, due_date__month=today.month).first()
        or unpaid.first()
    )

    this_month_due = this_month_schedule.amount_due if this_month_schedule else Decimal("0.00")
    this_month_due_date = this_month_schedule.due_date if this_month_schedule else None
    this_month_installment_number = (
        this_month_schedule.installment_number if this_month_schedule else None
    )

    return {
        "total_outstanding": total_outstanding.quantize(Decimal("0.01")),
        "this_month_due": this_month_due.quantize(Decimal("0.01")),
        "this_month_due_date": this_month_due_date,
        "this_month_installment_number": this_month_installment_number,
        "installments_remaining": unpaid.count(),
    }