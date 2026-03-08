"""
workouts/models.py

Django ORM models migrated from Flask SQLAlchemy.

Original Flask models:
- MuscleGroup(id, name)
- Exercise(id, name, muscle_group_id)
- Workout(id, user_id, name, date, notes, created_at)
- WorkoutMuscleGroup(id, workout_id, muscle_group_id)  ← bridge table
- WorkoutExercise(id, workout_id, exercise_id, sets, reps) ← bridge table

Key differences vs SQLAlchemy:
- ForeignKey syntax: db.ForeignKey('table.id') → models.ForeignKey(Model, on_delete=...)
- Relationships: db.relationship() → defined via ForeignKey + related_name
- No explicit bridge table needed for simple M2M → ManyToManyField
  BUT WorkoutExercise has extra fields (sets, reps) → keep as explicit model with 'through'
"""

from django.db import models
from django.conf import settings


class MuscleGroup(models.Model):
    """
    Predefined muscle group (e.g., Quadriceps, Glutes, Back).
    Seeded once via management command.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Exercise(models.Model):
    """
    Individual exercise belonging to one primary MuscleGroup.

    Note: reps stored as String in original Flask app ("8-10", "12-15+")
    to support rep ranges - we keep this logic in WorkoutExercise.
    """
    name = models.CharField(max_length=100)
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE,
        related_name='exercises'
    )

    class Meta:
        ordering = ['muscle_group__name', 'name']

    def __str__(self):
        return f'{self.name} ({self.muscle_group.name})'


class Workout(models.Model):
    """
    A training session belonging to a user.

    Relationships:
    - user: ForeignKey → CustomUser (each workout owned by one user)
    - muscle_groups: ManyToMany via WorkoutMuscleGroup (simple M2M without extras)
    - exercises: ManyToMany via WorkoutExercise (M2M WITH extra fields: sets, reps)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    name = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Simple M2M for muscle groups (no extra data on the link)
    muscle_groups = models.ManyToManyField(
        MuscleGroup,
        through='WorkoutMuscleGroup',
        related_name='workouts'
    )

    # M2M with extra data (sets, reps) → explicit through model
    exercises = models.ManyToManyField(
        Exercise,
        through='WorkoutExercise',
        related_name='workouts'
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.name} - {self.date} ({self.user.username})'


class WorkoutMuscleGroup(models.Model):
    """
    Bridge table: Workout ↔ MuscleGroup.

    Equivalent to Flask's WorkoutMuscleGroup.
    Using explicit 'through' model keeps it consistent with Flask structure
    and allows adding fields later (e.g., primary/secondary muscle flag).
    """
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='workout_muscle_groups'
    )
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE,
        related_name='workout_muscle_groups'
    )

    class Meta:
        unique_together = ('workout', 'muscle_group')

    def __str__(self):
        return f'{self.workout.name} → {self.muscle_group.name}'


class WorkoutExercise(models.Model):
    """
    Bridge table: Workout ↔ Exercise with extra workout-specific data.

    Critical: stores sets and reps PER workout, not globally on Exercise.
    Same exercise can appear in different workouts with different sets/reps.

    Reps stored as String to support ranges: "8-10", "12-15", "20+".
    """
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='workout_exercises'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='workout_exercises'
    )
    sets = models.PositiveIntegerField(default=3)
    reps = models.CharField(max_length=20, default='8-10')

    class Meta:
        unique_together = ('workout', 'exercise')

    def __str__(self):
        return f'{self.workout.name} | {self.exercise.name}: {self.sets}x{self.reps}'
