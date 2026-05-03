from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from config.permissions import IsAdminUserCustom
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from api.wallet.serializers import WalletSummarySerializer
from rest_framework import status, permissions
from .models import User, UserProfile
from .serializers import (
    CustomTokenObtainPairSerializer, UserListSerializer,
    UserRegistrationSerializer, UserProfileSerializer,
    AdminUserDetailSerializer, get_loan_eligibility, get_active_loan_summary,
    UserProfileInlineSerializer, ProfilePictureSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .tasks import send_verification_email, send_password_code
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from api.utils.cloudinary import upload_avatar

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

        response = Response({
            "message": "Email verified successfully.",
            "access": str(refresh.access_token)
        }, status=200)

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24,
        )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        refresh = response.data.get("refresh")

        if refresh:
            response.set_cookie(
                key="refresh",
                value=refresh,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60 * 60 * 24 * 3,
            )
            response.data.pop("refresh", None)

        return response


class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found in cookies"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)

        new_refresh = response.data.get("refresh")

        if new_refresh:
            response.set_cookie(
                key="refresh",
                value=new_refresh,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60 * 60 * 24 * 3,
            )
            response.data.pop("refresh", None)

        return response


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            wallet = user.wallet
        except ObjectDoesNotExist:
            wallet = None

        wallet_data = WalletSummarySerializer(wallet).data if wallet else None
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile_data = UserProfileInlineSerializer(profile).data

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
                "membership_id": user.membership_id,
                "avatar_url": profile.avatar_url or None,
            },
            "profile": profile_data,
            "wallet": wallet_data,
            "loan_eligibility": get_loan_eligibility(user),
            "active_loan": get_active_loan_summary(user),  # null if no active loan
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


class ProfilePictureUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
 
    def post(self, request):
        serializer = ProfilePictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        image_file = serializer.validated_data["image"]
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
 
        avatar_url = upload_avatar(image_file, request.user.id)
        profile.avatar_url = avatar_url
        profile.save(update_fields=["avatar_url", "updated_at"])
 
        return Response(
            {"avatar_url": avatar_url},
            status=status.HTTP_200_OK,
        )

class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUserCustom]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = User.objects.filter(is_admin=False).order_by("-id")
        email = self.request.query_params.get("email")
        if email:
            qs = qs.filter(email__iexact=email)
        return qs


class AdminUserDetailByEmailView(APIView):
    """GET /users/get-users/by-email/?email=user@example.com"""
    permission_classes = [IsAdminUserCustom]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email__iexact=email)
        return Response(AdminUserDetailSerializer(user).data, status=status.HTTP_200_OK)


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
        code = user.generate_verification_code()
        send_password_code(user.email, code)

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

        user.verification_code = None
        user.code_expiry = None
        user.save()

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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie("refresh")
        return response