from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.wallet.models import Wallet
from api.wallet.serializers import WalletSummarySerializer
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import  User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'gender', 'full_name', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        is_admin = validated_data.pop('is_admin', False)
        user = User.objects.create_user(
            **validated_data,
            is_active=False 
        )
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        # Fetch wallet safely
        try:
            wallet = user.wallet
        except ObjectDoesNotExist:
            wallet = None

        wallet_data = None
        if wallet:
            wallet_data = WalletSummarySerializer(wallet).data

        # Add extra response data
        data.update({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
            },
            "wallet": wallet_data
        })

        return data