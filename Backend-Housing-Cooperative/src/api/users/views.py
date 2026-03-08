from rest_framework.generics import ListAPIView, RetrieveAPIView
from config.permissions import IsAdminUserCustom
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from api.wallet.serializers import WalletSummarySerializer
from rest_framework import status, permissions
from .models import User, UserProfile
from .serializers import CustomTokenObtainPairSerializer, UserListSerializer, UserRegistrationSerializer, UserProfileSerializer, AdminUserDetailSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.parsers import MultiPartParser, FormParser
from .tasks import send_verification_email, send_password_code
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            code = user.generate_verification_code()
            send_verification_email(user.email, code)

            if user.is_admin:
                return Response(
                    {"message": "Admin user created successfully, email sent"},
                    status=status.HTTP_201_CREATED
                )

            return Response({"message": "Email sent"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)

        code = user.generate_verification_code()

        send_verification_email(user.email, code)

        return Response({"message": "Verification code resent"}, status=status.HTTP_200_OK)
    
class VerifyCodeView(APIView):
     def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if user.verification_code != code:
            return Response({"error": "Invalid verification code."}, status=400)

        if timezone.now() > user.code_expiry:
            return Response({"error": "Verification code expired."}, status=400)

        user.is_active = True
        user.verification_code = None
        user.email_verified = True
        user.code_expiry = None
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Email verified successfully.",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=200)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            wallet = user.wallet
        except ObjectDoesNotExist:
            wallet = None

        wallet_data = WalletSummarySerializer(wallet).data if wallet else None

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
                "membership_id": user.membership_id
            },
            "wallet": wallet_data
        }, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile(self, user):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self.get_profile(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if not created:
            return Response(
                {"error": "Profile already exists. Use PATCH to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = self.get_profile(request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUserCustom]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return User.objects.filter(is_admin=False).order_by("-id")

class UserDetailByIdView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserDetailSerializer
    permission_classes = [IsAdminUserCustom]
    lookup_field = "id"
    
class ForgotPasswordRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, email=email)
        
        code = user.generate_verification_code()  # reuse existing method
        send_password_code(user.email, code)  # reuse existing task
        
        return Response({"message": "Password reset code sent"}, status=status.HTTP_200_OK)


class ForgotPasswordVerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.verification_code != code:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() > user.code_expiry:
            return Response({"error": "Verification code expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Clear code and mark as verified — but don't activate account here
        user.verification_code = None
        user.code_expiry = None
        user.save()

        # Issue a short-lived token to authorize the password reset step
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Code verified. You may now reset your password.",
            "reset_token": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


class ForgotPasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)