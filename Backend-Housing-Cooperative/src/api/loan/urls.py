from django.urls import path
from . import views

urlpatterns = [
    # User
    path("preview/", views.LoanPreviewView.as_view()),
    path("apply/", views.LoanApplyView.as_view()),
    path("", views.UserLoanListView.as_view()),
    path("<uuid:uid>/", views.UserLoanDetailView.as_view()),
    path("<uuid:uid>/repay/", views.LoanRepayView.as_view()),

    # Admin
    path("admin/", views.AdminLoanListView.as_view()),
    path("admin/<uuid:uid>/", views.AdminLoanDetailView.as_view()),
    path("admin/<uuid:uid>/approve/", views.AdminApproveLoanView.as_view()),
    path("admin/<uuid:uid>/reject/", views.AdminRejectLoanView.as_view()),
]