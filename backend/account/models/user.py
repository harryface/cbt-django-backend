from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = False
        user.is_staff = False
        user.role = "student"
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.role = "examiner"
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """Create customuser and
    assign UserModelManager as the default object manager."""

    ROLE_CHOICES = (("teacher", "teacher"), ("student", "student"))

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES, default="student")

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name
