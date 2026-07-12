from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the primary identifier instead of username.

    This model extends Django's AbstractBaseUser and PermissionsMixin to provide
    a custom authentication system where users log in with their email address.
    It includes basic user information and integrates with Django's permission
    framework.
    """

    name = models.CharField("name", max_length=50)
    email = models.EmailField("email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField(blank=True, upload_to="public/users")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return f"{self.name} ({self.email})"
