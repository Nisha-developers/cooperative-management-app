from django.urls import path
from . import views

urlpatterns = [
    # User
    path("preview/", views.RentPreviewView.as_view(), name="rent-preview"),
    path("apply/", views.RentApplyView.as_view(), name="rent-apply"),
    path("", views.UserRentListView.as_view(), name="rent-list"),
    path("<uuid:uid>/", views.UserRentDetailView.as_view(), name="rent-detail"),

    # Admin
    path("admin/", views.AdminRentListView.as_view(), name="admin-rent-list"),
    path("admin/<uuid:uid>/", views.AdminRentDetailView.as_view(), name="admin-rent-detail"),
    path("admin/<uuid:uid>/approve/", views.AdminApproveRentView.as_view(), name="admin-rent-approve"),
    path("admin/<uuid:uid>/reject/", views.AdminRejectRentView.as_view(), name="admin-rent-reject"),
]
