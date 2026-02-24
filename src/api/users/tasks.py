# from celery import shared_task
# import requests
# from django.conf import settings

# from django.core.mail import send_mail

# @shared_task
# def send_verification_email(to_email, code):
#     send_mail(
#         subject="Verify Your Email",
#         message=f"Your verification code is: {code}. It will expire in 3 minutes",
#         from_email=f"App Team <noreply@myapp.com>",
#         recipient_list=[to_email],
#         fail_silently=False,
#     )

from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(to_email, code):
    send_mail(
        subject="Verify Your Email",
        message=f"Your verification code is: {code}. It will expire in 3 minutes",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )
