"""
users/models.py

Custom User model extending Django's AbstractUser.
Profile model with OneToOneField for profile picture (UCD methodology).
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    """
    Extended user model inheriting from Django's AbstractUser.

    Inherits all standard Django auth fields (username, email, password,
    first_name, last_name, is_active, is_staff, date_joined).

    Additional fields:
    - email: made unique and required
    - bio: personal description for the profile page
    - phone: contact details as required by the UCD assessment
    """

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.email})'


User = get_user_model()


class Profile(models.Model):
    """
    Profile model with OneToOneField to CustomUser.

    Stores the user's profile picture.
    Automatically created via signals when a new user registers.
    Images are resized to a maximum of 300x300 pixels on save.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='images/default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Override save to resize profile images larger than 300px.
        Keeps aspect ratio using Pillow's thumbnail method.
        On Render.com, image files may not be accessible — errors are caught silently.
        """
        super().save(*args, **kwargs)
        try:
            from PIL import Image
            with Image.open(self.image.path) as img:
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.image.path)
        except (FileNotFoundError, OSError):
            pass