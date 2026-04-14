from django.urls import path

from .views import (
    AdminApproveTransactionView,
    AdminTransactionListView,
    AdminProofUploadView,
    AdminRejectTransactionView,
    ClientProofUploadView,
    WalletCreditView,
    WalletDebitView,
    WalletDetailView,
    WalletTransactionHistoryView,
    WalletTransactionListView,
)

urlpatterns = [
    # Client
    path("", WalletDetailView.as_view(), name="wallet-summary"),
    path("full/", WalletDetailView.as_view(), {"full": True}, name="wallet-full"),
    path("transactions/", WalletTransactionListView.as_view(), name="wallet-transactions"),
    path("transactions/history/", WalletTransactionHistoryView.as_view(), name="wallet-history"),
    path("credit/", WalletCreditView.as_view(), name="wallet-credit"),
    path("debit/", WalletDebitView.as_view(), name="wallet-debit"),
    path("transactions/<uuid:uid>/proof/", ClientProofUploadView.as_view(), name="wallet-client-proof"),
    # Admin
    path("admin/transactions/", AdminTransactionListView.as_view(), name="admin-wallet-transactions"),
    path("admin/transactions/<uuid:uid>/approve/", AdminApproveTransactionView.as_view(), name="admin-wallet-approve"),
    path("admin/transactions/<uuid:uid>/reject/", AdminRejectTransactionView.as_view(), name="admin-wallet-reject"),
    path("admin/transactions/<uuid:uid>/proof/", AdminProofUploadView.as_view(), name="admin-wallet-proof"),
]