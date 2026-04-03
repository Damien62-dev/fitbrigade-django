"""
workouts/tests.py

Unit tests for the workouts app.
Covers: models, views, CRUD operations.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MuscleGroup, Exercise, Workout, WorkoutMuscleGroup, WorkoutExercise
import datetime

User = get_user_model()


class MuscleGroupModelTest(TestCase):
    """Tests for the MuscleGroup model."""

    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name='Quadriceps')

    def test_muscle_group_str(self):
        self.assertEqual(str(self.muscle_group), 'Quadriceps')

    def test_muscle_group_creation(self):
        self.assertEqual(MuscleGroup.objects.count(), 1)


class ExerciseModelTest(TestCase):
    """Tests for the Exercise model."""

    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name='Back')
        self.exercise = Exercise.objects.create(
            name='Deadlift',
            muscle_group=self.muscle_group
        )

    def test_exercise_str(self):
        self.assertIn('Deadlift', str(self.exercise))

    def test_exercise_muscle_group(self):
        self.assertEqual(self.exercise.muscle_group.name, 'Back')


class WorkoutModelTest(TestCase):
    """Tests for the Workout model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.workout = Workout.objects.create(
            user=self.user,
            name='Leg Day',
            date=datetime.date.today()
        )

    def test_workout_str(self):
        self.assertIn('Leg Day', str(self.workout))

    def test_workout_belongs_to_user(self):
        self.assertEqual(self.workout.user, self.user)


class WorkoutViewsTest(TestCase):
    """Tests for workout views — authentication and CRUD."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.workout = Workout.objects.create(
            user=self.user,
            name='Test Workout',
            date=datetime.date.today()
        )

    def test_home_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('workouts:home'))
        self.assertEqual(response.status_code, 302)

    def test_home_accessible_if_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('workouts:home'))
        self.assertEqual(response.status_code, 200)

    def test_index_accessible_without_login(self):
        response = self.client.get(reverse('workouts:index'))
        self.assertEqual(response.status_code, 200)

    def test_create_workout_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('workouts:create_workout'))
        self.assertEqual(response.status_code, 200)

    def test_create_workout_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('workouts:create_workout'), {
            'name': 'New Workout',
            'date': datetime.date.today(),
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Workout.objects.filter(name='New Workout').exists())

    def test_delete_workout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('workouts:delete_workout',
            args=[self.workout.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Workout.objects.filter(id=self.workout.id).exists())

    def test_user_cannot_access_other_user_workout(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('workouts:workout_detail',
            args=[self.workout.id]))
        self.assertEqual(response.status_code, 404)