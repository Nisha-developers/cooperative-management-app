"""
Email notification helpers for all important system actions.
Each function sends a plain-text email using Django's send_mail.
"""
from django.core.mail import send_mail
from django.conf import settings

FROM = settings.DEFAULT_FROM_EMAIL


# ── Auth ──────────────────────────────────────────────────────────────────────

def send_verification_email(to_email: str, code: str):
    send_mail(
        subject="Verify Your Email — Bethel Housing Cooperative",
        message=(
            f"Welcome to Bethel Housing Cooperative!\n\n"
            f"Your email verification code is: {code}\n"
            f"This code expires in 3 minutes.\n\n"
            f"If you did not create an account, please ignore this email."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_password_code(to_email: str, code: str):
    send_mail(
        subject="Password Reset Code — Bethel Housing Cooperative",
        message=(
            f"You requested a password reset.\n\n"
            f"Your reset code is: {code}\n"
            f"This code expires in 3 minutes.\n\n"
            f"If you did not request this, please ignore this email."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


# ── Loan ──────────────────────────────────────────────────────────────────────

def send_loan_application_received(to_email: str, membership_id: str, principal, tenure_months: int):
    send_mail(
        subject="Loan Application Received — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"We have received your loan application for ₦{principal:,.2f} "
            f"over {tenure_months} month(s).\n\n"
            f"Your application is currently under review. "
            f"You will be notified once a decision has been made.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_loan_approved(to_email: str, membership_id: str, principal, monthly_installment, tenure_months: int):
    send_mail(
        subject="Loan Approved — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your loan application of ₦{principal:,.2f} has been APPROVED "
            f"and disbursed to your wallet.\n\n"
            f"Repayment Details:\n"
            f"  Monthly Installment : ₦{monthly_installment:,.2f}\n"
            f"  Tenure              : {tenure_months} month(s)\n\n"
            f"Please ensure your wallet is funded before each monthly due date "
            f"to avoid penalties.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_loan_rejected(to_email: str, membership_id: str, rejection_reason: str):
    send_mail(
        subject="Loan Application Declined — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"We regret to inform you that your loan application has been DECLINED.\n\n"
            f"Reason: {rejection_reason}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_loan_installment_paid(
    to_email: str, membership_id: str,
    installment_number: int, tenure_months: int,
    amount_paid, remaining_count: int,
):
    if remaining_count == 0:
        extra = "Congratulations — your loan is now FULLY PAID!"
    else:
        extra = f"{remaining_count} installment(s) remaining."

    send_mail(
        subject=f"Loan Installment {installment_number} Paid — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Installment {installment_number} of {tenure_months} has been successfully "
            f"deducted from your wallet.\n\n"
            f"  Amount Paid : ₦{amount_paid:,.2f}\n\n"
            f"{extra}\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_loan_installment_failed(
    to_email: str, membership_id: str,
    installment_number: int, amount_due, wallet_balance,
):
    send_mail(
        subject="Loan Installment Payment Failed — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"We were unable to deduct installment {installment_number} from your wallet.\n\n"
            f"  Amount Due      : ₦{amount_due:,.2f}\n"
            f"  Wallet Balance  : ₦{wallet_balance:,.2f}\n\n"
            f"Please fund your wallet immediately to avoid penalties and loan default.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


# ── Purchase ──────────────────────────────────────────────────────────────────

def send_purchase_application_received(to_email: str, membership_id: str, listing_title: str, purchase_type: str):
    send_mail(
        subject="Purchase Application Received — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"We have received your {purchase_type.lower()} purchase application for:\n"
            f"  Property: {listing_title}\n\n"
            f"Your application is under review and you will be notified once approved.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_purchase_approved(to_email: str, membership_id: str, listing_title: str, purchase_type: str, amount_deducted):
    send_mail(
        subject="Purchase Approved — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your {purchase_type.lower()} purchase application for '{listing_title}' has been APPROVED.\n\n"
            f"  Amount Deducted: ₦{amount_deducted:,.2f}\n\n"
            f"The property has been reserved in your name. "
            f"Please check your purchase details in the app.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_purchase_rejected(to_email: str, membership_id: str, listing_title: str, remark: str):
    send_mail(
        subject="Purchase Application Declined — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your purchase application for '{listing_title}' has been DECLINED.\n\n"
            f"Reason: {remark or 'No reason provided.'}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_purchase_completed(to_email: str, membership_id: str, listing_title: str):
    send_mail(
        subject="Property Purchase Complete — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Congratulations! Your purchase of '{listing_title}' is now COMPLETE.\n\n"
            f"All installments have been cleared and the property is fully yours.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_purchase_installment_paid(
    to_email: str, membership_id: str,
    listing_title: str, installment_number: int,
    tenure_months: int, amount_paid, remaining_count: int,
):
    if remaining_count == 0:
        extra = "All installments cleared — the property is now fully yours!"
    else:
        extra = f"{remaining_count} installment(s) remaining."

    send_mail(
        subject=f"Property Installment {installment_number} Paid — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Installment {installment_number} of {tenure_months} for '{listing_title}' "
            f"has been successfully paid.\n\n"
            f"  Amount Paid : ₦{amount_paid:,.2f}\n\n"
            f"{extra}\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


# ── Rent ──────────────────────────────────────────────────────────────────────

def send_rent_application_received(to_email: str, membership_id: str, listing_title: str, duration_days: int, total_cost):
    send_mail(
        subject="Rent Application Received — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"We have received your rent application for:\n"
            f"  Property     : {listing_title}\n"
            f"  Duration     : {duration_days} day(s)\n"
            f"  Total Cost   : ₦{total_cost:,.2f}\n\n"
            f"Your application is under review and you will be notified once approved.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_rent_approved(to_email: str, membership_id: str, listing_title: str, start_date, end_date, total_cost):
    send_mail(
        subject="Rent Application Approved — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your rent application for '{listing_title}' has been APPROVED.\n\n"
            f"  Rental Period : {start_date} to {end_date}\n"
            f"  Total Charged : ₦{total_cost:,.2f}\n\n"
            f"The amount has been deducted from your wallet. Enjoy your stay!\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_rent_rejected(to_email: str, membership_id: str, listing_title: str, rejection_reason: str):
    send_mail(
        subject="Rent Application Declined — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your rent application for '{listing_title}' has been DECLINED.\n\n"
            f"Reason: {rejection_reason or 'No reason provided.'}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


# ── Wallet ────────────────────────────────────────────────────────────────────

def send_wallet_funded(to_email: str, membership_id: str, amount, new_balance):
    send_mail(
        subject="Wallet Funded — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your wallet has been credited successfully.\n\n"
            f"  Amount Credited : ₦{amount:,.2f}\n"
            f"  New Balance     : ₦{new_balance:,.2f}\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_withdrawal_approved(to_email: str, membership_id: str, amount, new_balance):
    send_mail(
        subject="Withdrawal Approved — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your withdrawal request has been approved and processed.\n\n"
            f"  Amount Withdrawn : ₦{amount:,.2f}\n"
            f"  New Balance      : ₦{new_balance:,.2f}\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )


def send_withdrawal_rejected(to_email: str, membership_id: str, amount, rejection_reason: str):
    send_mail(
        subject="Withdrawal Declined — Bethel Housing Cooperative",
        message=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your withdrawal request of ₦{amount:,.2f} has been DECLINED.\n\n"
            f"Reason: {rejection_reason or 'No reason provided.'}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
        from_email=FROM,
        recipient_list=[to_email],
        fail_silently=False,
    )
