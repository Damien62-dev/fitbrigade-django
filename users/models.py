"""
users/models.py

Custom User model extending Django's AbstractUser.

Why a custom user? Best practice Django: always define AUTH_USER_MODEL
before the first migration. Allows adding profile fields later
(avatar, bio, etc.) without complex migrations.

Migrated from Flask's basic User(id, username, email, created_at).
Django's AbstractUser already provides: username, email, password (hashed),
first_name, last_name, is_active, is_staff, date_joined.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extended user model.

    Inherits all standard Django auth fields (username, email, password,
    first_name, last_name, is_active, is_staff, date_joined).

    Additional fields for the UCD assessment requirements:
    - bio: personal description (profile page)
    - avatar: profile picture
    - phone: contact details (assessment: "update personal and contact details")
    """

    email = models.EmailField(unique=True)  # Make email required & unique

    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.email})'
