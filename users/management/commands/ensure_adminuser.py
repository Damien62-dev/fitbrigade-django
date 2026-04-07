"""
Management command to create a superuser non-interactively.
Used during Render.com deployment via Build Command.
"""

import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser non-interactively if it does not exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ['DJANGO_SUPERUSER_USERNAME']
        email = os.environ['DJANGO_SUPERUSER_EMAIL']
        password = os.environ['DJANGO_SUPERUSER_PASSWORD']

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully"))
        else:
            self.stdout.write(f"Superuser '{username}' already exists")