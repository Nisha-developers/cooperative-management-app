from django.db import models, transaction
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast, Substr
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import random
from django.utils import timezone
from datetime import timedelta


class UserGender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=20,
        choices=UserGender.choices,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expiry = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    membership_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    def generate_verification_code(self):
        code = f"{random.randint(100000, 999999)}"
        self.verification_code = code
        self.code_expiry = timezone.now() + timedelta(minutes=3)
        self.save()
        return code

    def generate_membership_id(self):
        last_number = (
            User.objects
            .filter(membership_id__startswith="bethel")
            .annotate(
                number=Cast(
                    Substr("membership_id", 7),
                    IntegerField()
                )
            )
            .aggregate(Max("number"))
        )["number__max"]

        new_number = (last_number + 1) if last_number else 1000
        return f"bethel{new_number}"

    def save(self, *args, **kwargs):
        if not self.membership_id and not self.is_admin:
            with transaction.atomic():
                self.membership_id = self.generate_membership_id()
                super().save(*args, **kwargs)
                return
        super().save(*args, **kwargs)

    objects = CustomUserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar_url = models.TextField(
        blank=True,
        default="",
        help_text="Cloudinary URL for the user's profile picture",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Profile"