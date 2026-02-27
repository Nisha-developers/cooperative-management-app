from django.urls import path
from .views import CustomTokenObtainPairView, UserRegistrationView, ResendVerificationCodeView, VerifyCodeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('resend-code/', ResendVerificationCodeView.as_view(), name='resend-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
