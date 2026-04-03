"""
messaging/tests.py
Unit tests for the messaging app.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class MessageModelTest(TestCase):
    """Tests for the Message model."""

    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='testpass123'
        )
        self.recipient = User.objects.create_user(
            username='recipient',
            email='recipient@test.com',
            password='testpass123'
        )
        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject='Test Subject',
            body='Test body'
        )

    def test_message_str(self):
        self.assertIn('sender', str(self.message))
        self.assertIn('recipient', str(self.message))

    def test_message_default_not_read(self):
        self.assertFalse(self.message.is_read)

    def test_message_default_not_archived(self):
        self.assertFalse(self.message.is_archived)


class MessagingViewsTest(TestCase):
    """Tests for messaging views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='testpass123'
        )
        self.message = Message.objects.create(
            sender=self.other_user,
            recipient=self.user,
            subject='Hello',
            body='Hello there!'
        )

    def test_inbox_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 302)

    def test_inbox_accessible_if_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('messaging:send_message'), {
            'recipient': self.other_user.id,
            'subject': 'New Message',
            'body': 'Hello!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(subject='New Message').exists())

    def test_view_message_marks_as_read(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.get(reverse('messaging:view_message',
            args=[self.message.id]))
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

    def test_archive_message(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.get(reverse('messaging:archive_message',
            args=[self.message.id]))
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_archived)