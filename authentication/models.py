from typing import Optional

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

from shared.django import TimeStampMixin


class CustomUserManager(UserManager):
    """custom user manager"""

    def create_user(self, email, username=None, password=None, **kwargs):
        if not email:
            raise ValueError("Email field is requiered.")
        if not password:
            raise ValueError("Password field is requiered.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        super_user_payload: dict = {
            "is_superuser": True,
            "is_active": True,
            "is_staff": True,
        }
        return self.create_user(email, username, password, **super_user_payload)


class Role(TimeStampMixin):
    """user's Role which is used for giving permissions"""

    name = models.CharField(max_length=50)


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):
    """This is my custom User model"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    age = models.PositiveSmallIntegerField(null=True, default=2)
    phone = models.CharField(max_length=13, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # role = models.ForeignKey(null=True, default=)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    date_joined = models.DateTimeField(("date joined"), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    class Meta:
        # db_table = "users"
        verbose_name_plural = "Users"
