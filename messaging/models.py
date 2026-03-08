"""
messaging/models.py

Inbox system: users can send, receive, and archive messages.
Scope for today: model defined, migration ready.
Views/templates in a future session.
"""

from django.db import models
from django.conf import settings


class Message(models.Model):
    """
    A direct message between two users.

    sender → recipient, with archive flag per recipient.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'From {self.sender} → {self.recipient}: {self.subject}'
