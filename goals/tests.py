"""
goals/tests.py
Unit tests for the goals app.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Goal
import datetime

User = get_user_model()


class GoalModelTest(TestCase):
    """Tests for the Goal model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.goal = Goal.objects.create(
            user=self.user,
            name='Bench 100kg',
            notes='My first big goal'
        )

    def test_goal_str(self):
        self.assertIn('Bench 100kg', str(self.goal))

    def test_goal_belongs_to_user(self):
        self.assertEqual(self.goal.user, self.user)

    def test_goal_optional_fields_null(self):
        self.assertIsNone(self.goal.deadline)
        self.assertIsNone(self.goal.target_weight)
        self.assertIsNone(self.goal.target_reps)


class GoalViewsTest(TestCase):
    """Tests for goal views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.goal = Goal.objects.create(
            user=self.user,
            name='Test Goal',
            notes='Test notes'
        )

    def test_goals_list_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('goals:goals_list'))
        self.assertEqual(response.status_code, 302)

    def test_goals_list_accessible_if_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('goals:goals_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_goal_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('goals:create_goal'), {
            'name': 'New Goal',
            'notes': 'Some notes',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Goal.objects.filter(name='New Goal').exists())

    def test_delete_goal(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('goals:delete_goal',
            args=[self.goal.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Goal.objects.filter(id=self.goal.id).exists())

    def test_user_cannot_access_other_user_goal(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('goals:goal_detail',
            args=[self.goal.id]))
        self.assertEqual(response.status_code, 404)