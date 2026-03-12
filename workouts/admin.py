from django.contrib import admin
from .models import MuscleGroup, Exercise, Workout, WorkoutMuscleGroup, WorkoutExercise

admin.site.register(MuscleGroup)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(WorkoutMuscleGroup)
admin.site.register(WorkoutExercise)