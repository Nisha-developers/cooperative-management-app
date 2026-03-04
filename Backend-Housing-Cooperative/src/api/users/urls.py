from django.urls import path
from .views import CustomTokenObtainPairView, UserDetailView, UserProfileView, UserRegistrationView, ResendVerificationCodeView, VerifyCodeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile')
]
