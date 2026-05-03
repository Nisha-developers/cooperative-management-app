from django.urls import path
from .views import (
    AdminUserDetailByEmailView,
    CustomTokenObtainPairView,
    ForgotPasswordRequestView,
    ForgotPasswordVerifyCodeView,
    ForgotPasswordResetView,
    UserDetailByIdView,
    UserDetailView,
    UserListView,
    UserProfileView,
    UserRegistrationView,
    ResendVerificationCodeView,
    VerifyCodeView,
    ProfilePictureUploadView,
    LogoutView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("forgot-password/", ForgotPasswordRequestView.as_view()),
    path("forgot-password/verify/", ForgotPasswordVerifyCodeView.as_view()),
    path("forgot-password/reset/", ForgotPasswordResetView.as_view()),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/avatar/', ProfilePictureUploadView.as_view(), name='profile-avatar'),
    path("get-users/", UserListView.as_view(), name="user-list"),
    path("get-users/by-email/", AdminUserDetailByEmailView.as_view(), name="user-detail-by-email"),
    path("get-users/<int:id>/", UserDetailByIdView.as_view(), name="user-detail-by-id"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
