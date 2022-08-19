from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

from shared.django import TimeStampMixin

DEFAULT_ROLES = {
    "admin": 1,
    "user": 2,
}


class CustomUserManager(UserManager):
    """custom user manager"""

    def create_user(self, email, username=None, password=None, **kwargs):
        if email is None:
            raise ValueError("Email field is requiered.")
        if password is None:
            raise ValueError("Password field is requiered.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        _payload = kwargs
        superuser_payload: dict = {
            "is_superuser": True,
            "is_active": True,
            "is_staff": True,
            "role_id": DEFAULT_ROLES["admin"],
        }
        _payload.update(superuser_payload)
        return self.create_user(email, username, password, **_payload)


class Role(TimeStampMixin):
    """user's Role which is used for giving permissions"""

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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

    role = models.ForeignKey(
        Role,
        null=True,
        default=DEFAULT_ROLES["user"],
        on_delete=models.SET_NULL,
        related_name="users",
    )

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

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({"id": self.pk, "exp": int(dt.strftime("%s"))}, settings.SECRET_KEY, algorithm="HS256")

        return token
