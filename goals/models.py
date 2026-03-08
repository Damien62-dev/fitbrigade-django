"""
goals/models.py

Django ORM model migrated from Flask SQLAlchemy Goal model.

Original Flask model:
    Goal(id, user_id, exercise_id, name, target_weight, target_reps,
         deadline, notes, created_at)

exercise_id is nullable → goal can be general (not exercise-specific).
"""

from django.db import models
from django.conf import settings
from workouts.models import Exercise


class Goal(models.Model):
    """
    A fitness objective set by a user.

    Can be exercise-specific (e.g., "Bench press 100kg")
    or general (e.g., "Run a marathon").
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    # Nullable: goal doesn't have to be tied to a specific exercise
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goals'
    )
    name = models.CharField(max_length=100)
    target_weight = models.FloatField(null=True, blank=True)
    target_reps = models.PositiveIntegerField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['deadline', '-created_at']

    def __str__(self):
        return f'{self.name} ({self.user.username})'
