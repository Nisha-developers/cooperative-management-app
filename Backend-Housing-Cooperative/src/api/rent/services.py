from datetime import date, timedelta
from decimal import Decimal

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

from .models import Rent, RentStatus


def approve_rent(rent: Rent, admin_user):
    """
    Admin approval flow:
    1. Debit total rent cost from user's wallet.
    2. Set rental start/end dates (start = today, end = today + duration_days).
    3. Mark listing RENTED.
    4. Mark rent ACTIVE.
    """
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=rent.user)
        listing = rent.listing

        if wallet.balance < rent.total_rent_cost:
            raise ValueError(
                f"Insufficient wallet balance. ₦{rent.total_rent_cost:,.2f} required, "
                f"₦{wallet.balance:,.2f} available."
            )

        tx = WalletTransaction.objects.create(
            wallet=wallet,
            type=WalletTransactionType.DEBIT,
            source=WalletTransactionSource.PURCHASE,
            status=WalletTransactionStatus.CONFIRMED,
            amount=rent.total_rent_cost,
            remark=(
                f"Rent payment — {listing.title} "
                f"({rent.duration_days} days, Rent #{rent.uid})"
            ),
            created_by=admin_user,
            confirmed_by=admin_user,
            confirmed_at=timezone.now(),
        )
        wallet.balance -= rent.total_rent_cost
        wallet.save(update_fields=["balance", "updated_on"])

        today = date.today()
        rent.start_date = today
        rent.end_date = today + timedelta(days=rent.duration_days)
        rent.status = RentStatus.ACTIVE
        rent.approved_by = admin_user
        rent.approved_at = timezone.now()
        rent.wallet_transaction = tx
        rent.save()

        listing.status = ListingStatus.RENTED
        listing.save(update_fields=["status", "updated_at"])
