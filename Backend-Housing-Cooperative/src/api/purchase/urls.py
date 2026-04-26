from django.urls import path
from . import views

urlpatterns = [
    # ── User ────────────────────────────────────────────────────────────────
    path("preview/", views.PurchasePreviewView.as_view(), name="purchase-preview"),
    path("apply/", views.PurchaseApplyView.as_view(), name="purchase-apply"),
    path("", views.UserPurchaseListView.as_view(), name="purchase-list"),
    path("<uuid:uid>/", views.UserPurchaseDetailView.as_view(), name="purchase-detail"),
    path("<uuid:uid>/pay/", views.PurchasePayInstallmentView.as_view(), name="purchase-pay"),

    # ── Admin ────────────────────────────────────────────────────────────────
    path("admin/", views.AdminPurchaseListView.as_view(), name="admin-purchase-list"),
    path("admin/<uuid:uid>/", views.AdminPurchaseDetailView.as_view(), name="admin-purchase-detail"),
    path("admin/<uuid:uid>/approve/", views.AdminApprovePurchaseView.as_view(), name="admin-purchase-approve"),
    path("admin/<uuid:uid>/reject/", views.AdminRejectPurchaseView.as_view(), name="admin-purchase-reject"),
]