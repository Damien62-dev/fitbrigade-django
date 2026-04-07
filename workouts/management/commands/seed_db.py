"""
Management command to seed the database with muscle groups and exercises.
Used during Render.com deployment via Build Command.
"""

from django.core.management.base import BaseCommand
from workouts.models import MuscleGroup, Exercise


class Command(BaseCommand):
    help = 'Seed the database with muscle groups and exercises'

    def handle(self, *args, **kwargs):
        muscle_groups_data = {
            'Abs': ['Bicycle Crunches', 'Crunches', 'Leg Raises', 'Planks', 'Russian Twists'],
            'Back': ['Barbell Row', 'Deadlift', 'Lat Pull-down', 'Pull-ups', 'Seated Cable Row', 'T-bar Row'],
            'Biceps': ['Barbell Curl', 'Cable Curl', 'Concentration Curl', 'Hammer Curl', 'Preacher Curl'],
            'Calves': ['Calf Press on Leg Machine', 'Seated Calf Raise', 'Standing Calf Raise'],
            'Chest': ['Bench Press', 'Cable Crossovers', 'Chest Fly', 'Dips', 'Incline Press', 'Push-ups'],
            'Forearms': ["Farmer's Walk", 'Reverse Curl', 'Wrist Curl'],
            'Glutes': ['Bulgarian Split Squat', 'Glute Bridge', 'Hip Thrust', 'Sumo Deadlift'],
            'Hamstrings': ['Good Morning', 'Leg Curl', 'Romanian Deadlift', 'Stiff-leg Deadlift'],
            'Quadriceps': ['Back Squat', 'Front Squat', 'Hack Squat', 'Leg Extension', 'Leg Press', 'Lunges'],
            'Shoulders': ['Arnold Press', 'Face Pull', 'Lateral Raise', 'Overhead Press', 'Upright Row'],
            'Traps': ['Face Pull', 'Rack Pull', 'Shrugs'],
            'Triceps': ['Close-grip Bench Press', 'Dips', 'Overhead Tricep Extension', 'Skull Crushers', 'Tricep Pushdown'],
        }

        for muscle_name, exercises in muscle_groups_data.items():
            mg, _ = MuscleGroup.objects.get_or_create(name=muscle_name)
            for exercise_name in exercises:
                Exercise.objects.get_or_create(name=exercise_name, muscle_group=mg)

        self.stdout.write(self.style.SUCCESS(
            f'Done! {MuscleGroup.objects.count()} muscle groups, {Exercise.objects.count()} exercises.'
        ))