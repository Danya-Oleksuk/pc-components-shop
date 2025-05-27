import uuid

from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.mail import send_mail

from pc_components_shop import settings


# class User(AbstractUser):
#     username = None
#     is_verified = models.BooleanField(default=False)
#     email = models.EmailField(unique=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.email


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def send_verification_email(self):
        send_mail(
            subject='Verify your email',
            message = f'Click the link to verify your email: http://localhost:8000/activate/{self.code}/',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False
        )