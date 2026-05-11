"""
Email notification helpers for all important system actions.
Each function sends an email using the Resend Python SDK.
"""
import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY
FROM = settings.DEFAULT_FROM_EMAIL


def _send(to_email: str, subject: str, body: str):
    """Internal helper — sends a plain-text email via Resend."""
    resend.Emails.send({
        "from": FROM,
        "to": to_email,
        "subject": subject,
        "html": f"<pre style='font-family:sans-serif;white-space:pre-wrap'>{body}</pre>",
    })


# ── Auth ──────────────────────────────────────────────────────────────────────

def send_verification_email(to_email: str, code: str):
    _send(
        to_email,
        subject="Verify Your Email — Bethel Housing Cooperative",
        body=(
            f"Welcome to Bethel Housing Cooperative!\n\n"
            f"Your email verification code is: {code}\n"
            f"This code expires in 3 minutes.\n\n"
            f"If you did not create an account, please ignore this email."
        ),
    )


def send_password_code(to_email: str, code: str):
    _send(
        to_email,
        subject="Password Reset Code — Bethel Housing Cooperative",
        body=(
            f"You requested a password reset.\n\n"
            f"Your reset code is: {code}\n"
            f"This code expires in 3 minutes.\n\n"
            f"If you did not request this, please ignore this email."
        ),
    )


# ── Loan ──────────────────────────────────────────────────────────────────────

def send_loan_application_received(to_email: str, membership_id: str, principal, tenure_months: int):
    _send(
        to_email,
        subject="Loan Application Received — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"We have received your loan application for ₦{principal:,.2f} "
            f"over {tenure_months} month(s).\n\n"
            f"Your application is currently under review. "
            f"You will be notified once a decision has been made.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )


def send_loan_approved(to_email: str, membership_id: str, principal, monthly_installment, tenure_months: int):
    _send(
        to_email,
        subject="Loan Approved — Bethel Housing Cooperative",
        body=(
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
    )


def send_loan_rejected(to_email: str, membership_id: str, rejection_reason: str):
    _send(
        to_email,
        subject="Loan Application Declined — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"We regret to inform you that your loan application has been DECLINED.\n\n"
            f"Reason: {rejection_reason}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )


def send_loan_installment_paid(
    to_email: str, membership_id: str,
    installment_number: int, tenure_months: int,
    amount_paid, remaining_count: int,
):
    extra = "Congratulations — your loan is now FULLY PAID!" if remaining_count == 0 else f"{remaining_count} installment(s) remaining."
    _send(
        to_email,
        subject=f"Loan Installment {installment_number} Paid — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Installment {installment_number} of {tenure_months} has been successfully "
            f"deducted from your wallet.\n\n"
            f"  Amount Paid : ₦{amount_paid:,.2f}\n\n"
            f"{extra}\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )


def send_loan_installment_failed(
    to_email: str, membership_id: str,
    installment_number: int, amount_due, wallet_balance,
):
    _send(
        to_email,
        subject="Loan Installment Payment Failed — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"We were unable to deduct installment {installment_number} from your wallet.\n\n"
            f"  Amount Due      : ₦{amount_due:,.2f}\n"
            f"  Wallet Balance  : ₦{wallet_balance:,.2f}\n\n"
            f"Please fund your wallet immediately to avoid penalties and loan default.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )


# ── Purchase ──────────────────────────────────────────────────────────────────

def send_purchase_application_received(to_email: str, membership_id: str, listing_title: str, purchase_type: str):
    _send(
        to_email,
        subject="Purchase Application Received — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"We have received your {purchase_type.lower()} purchase application for:\n"
            f"  Property: {listing_title}\n\n"
            f"Your application is under review and you will be notified once approved.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


def send_purchase_approved(to_email: str, membership_id: str, listing_title: str, purchase_type: str, amount_deducted):
    _send(
        to_email,
        subject="Purchase Approved — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your {purchase_type.lower()} purchase application for '{listing_title}' has been APPROVED.\n\n"
            f"  Amount Deducted: ₦{amount_deducted:,.2f}\n\n"
            f"The property has been reserved in your name. "
            f"Please check your purchase details in the app.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


def send_purchase_rejected(to_email: str, membership_id: str, listing_title: str, remark: str):
    _send(
        to_email,
        subject="Purchase Application Declined — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your purchase application for '{listing_title}' has been DECLINED.\n\n"
            f"Reason: {remark or 'No reason provided.'}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


def send_purchase_completed(to_email: str, membership_id: str, listing_title: str):
    _send(
        to_email,
        subject="Property Purchase Complete — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Congratulations! Your purchase of '{listing_title}' is now COMPLETE.\n\n"
            f"All installments have been cleared and the property is fully yours.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


def send_purchase_installment_paid(
    to_email: str, membership_id: str,
    listing_title: str, installment_number: int,
    tenure_months: int, amount_paid, remaining_count: int,
):
    extra = "All installments cleared — the property is now fully yours!" if remaining_count == 0 else f"{remaining_count} installment(s) remaining."
    _send(
        to_email,
        subject=f"Property Installment {installment_number} Paid — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Installment {installment_number} of {tenure_months} for '{listing_title}' "
            f"has been successfully paid.\n\n"
            f"  Amount Paid : ₦{amount_paid:,.2f}\n\n"
            f"{extra}\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


# ── Rent ──────────────────────────────────────────────────────────────────────

def send_rent_application_received(to_email: str, membership_id: str, listing_title: str, duration_days: int, total_cost):
    _send(
        to_email,
        subject="Rent Application Received — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"We have received your rent application for:\n"
            f"  Property     : {listing_title}\n"
            f"  Duration     : {duration_days} day(s)\n"
            f"  Total Cost   : ₦{total_cost:,.2f}\n\n"
            f"Your application is under review and you will be notified once approved.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


def send_rent_approved(to_email: str, membership_id: str, listing_title: str, start_date, end_date, total_cost):
    _send(
        to_email,
        subject="Rent Application Approved — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your rent application for '{listing_title}' has been APPROVED.\n\n"
            f"  Rental Period : {start_date} to {end_date}\n"
            f"  Total Charged : ₦{total_cost:,.2f}\n\n"
            f"The amount has been deducted from your wallet. Enjoy your stay!\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


def send_rent_rejected(to_email: str, membership_id: str, listing_title: str, rejection_reason: str):
    _send(
        to_email,
        subject="Rent Application Declined — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your rent application for '{listing_title}' has been DECLINED.\n\n"
            f"Reason: {rejection_reason or 'No reason provided.'}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for choosing Bethel Housing Cooperative."
        ),
    )


# ── Wallet ────────────────────────────────────────────────────────────────────

def send_wallet_funded(to_email: str, membership_id: str, amount, new_balance):
    _send(
        to_email,
        subject="Wallet Funded — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your wallet has been credited successfully.\n\n"
            f"  Amount Credited : ₦{amount:,.2f}\n"
            f"  New Balance     : ₦{new_balance:,.2f}\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )


def send_withdrawal_approved(to_email: str, membership_id: str, amount, new_balance):
    _send(
        to_email,
        subject="Withdrawal Approved — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your withdrawal request has been approved and processed.\n\n"
            f"  Amount Withdrawn : ₦{amount:,.2f}\n"
            f"  New Balance      : ₦{new_balance:,.2f}\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )


def send_withdrawal_rejected(to_email: str, membership_id: str, amount, rejection_reason: str):
    _send(
        to_email,
        subject="Withdrawal Declined — Bethel Housing Cooperative",
        body=(
            f"Dear Member ({membership_id}),\n\n"
            f"Your withdrawal request of ₦{amount:,.2f} has been DECLINED.\n\n"
            f"Reason: {rejection_reason or 'No reason provided.'}\n\n"
            f"If you have questions, please contact our support team.\n\n"
            f"Thank you for banking with Bethel Housing Cooperative."
        ),
    )