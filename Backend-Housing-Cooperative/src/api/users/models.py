from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import random
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class UserGender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    
    gender = models.CharField(
        max_length=20, choices=UserGender.choices, null=True, blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expiry = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def generate_verification_code(self):
        code = f"{random.randint(100000, 999999)}"
        self.verification_code = code
        self.code_expiry = timezone.now() + timedelta(minutes=3)
        self.save()
        return code
    
    objects = CustomUserManager()
