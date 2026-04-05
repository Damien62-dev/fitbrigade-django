from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workout, MuscleGroup, Exercise, WorkoutMuscleGroup, WorkoutExercise


def index(request):
    """
    Public landing page for FitBrigade.
    Redirects authenticated users to their workout dashboard.
    """
    if request.user.is_authenticated:
        return redirect('workouts:home')
    return render(request, 'workouts/index.html')


@login_required
def home(request):
    """
    Display all workouts for the logged-in user.
    Workouts are ordered by date, most recent first.
    """
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workouts/home.html', {'workouts': workouts})


@login_required
def workout_detail(request, workout_id):
    """
    Display full details of a single workout.
    Exercises are grouped by muscle group for display.
    Returns 404 if the workout does not belong to the logged-in user.
    """
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    muscle_groups = workout.muscle_groups.all()
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)

    exercises_by_muscle = {}
    for we in workout_exercises:
        muscle_name = we.exercise.muscle_group.name
        if muscle_name not in exercises_by_muscle:
            exercises_by_muscle[muscle_name] = []
        exercises_by_muscle[muscle_name].append({
            'name': we.exercise.name,
            'sets': we.sets,
            'reps': we.reps
        })

    return render(request, 'workouts/workout_detail.html', {
        'workout': workout,
        'muscle_groups': muscle_groups,
        'exercises_by_muscle': exercises_by_muscle
    })


@login_required
def create_workout(request):
    """
    Handle creation of a new workout.
    GET: Display the workout creation form with all muscle groups and exercises.
    POST: Validate and save the workout, associated muscle groups and exercises.
    """
    muscle_groups = MuscleGroup.objects.all()
    exercises_by_muscle = {}
    for mg in muscle_groups:
        exercises_by_muscle[mg.name] = Exercise.objects.filter(muscle_group=mg)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        date_str = request.POST.get('date', '')
        notes = request.POST.get('notes', '').strip()

        if not name or not date_str:
            messages.error(request, 'Please fill in workout name and date.')
            return render(request, 'workouts/create_workout.html', {
                'muscle_groups': muscle_groups,
                'all_exercises': exercises_by_muscle
            })

        workout = Workout.objects.create(
            user=request.user,
            name=name,
            date=date_str,
            notes=notes if notes else None
        )

        selected_muscles = request.POST.getlist('muscle_groups')
        for muscle_name in selected_muscles:
            muscle_group = MuscleGroup.objects.filter(name=muscle_name).first()
            if muscle_group:
                WorkoutMuscleGroup.objects.create(workout=workout, muscle_group=muscle_group)

            selected_exercises = request.POST.getlist(f'exercises_{muscle_name}')
            for exercise_name in selected_exercises:
                exercise = Exercise.objects.filter(name=exercise_name).first()
                if exercise:
                    sets = request.POST.get(f'sets_{muscle_name}_{exercise_name}', '3')
                    reps = request.POST.get(f'reps_{muscle_name}_{exercise_name}', '8-10')
                    WorkoutExercise.objects.create(
                        workout=workout,
                        exercise=exercise,
                        sets=int(sets),
                        reps=reps
                    )

        messages.success(request, 'Workout created successfully!')
        return redirect('workouts:home')

    return render(request, 'workouts/create_workout.html', {
        'muscle_groups': muscle_groups,
        'all_exercises': exercises_by_muscle
    })


@login_required
def edit_workout(request, workout_id):
    """
    Handle editing of an existing workout.
    GET: Display the edit form pre-populated with current workout data.
    POST: Delete existing muscle groups and exercises, then save updated ones.
    Returns 404 if the workout does not belong to the logged-in user.
    """
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    muscle_groups = MuscleGroup.objects.all()
    exercises_by_muscle = {}
    for mg in muscle_groups:
        exercises_by_muscle[mg.name] = Exercise.objects.filter(muscle_group=mg)

    workout_muscle_groups = workout.muscle_groups.all()
    selected_muscle_names = set(mg.name for mg in workout_muscle_groups)

    workout_exercises = WorkoutExercise.objects.filter(workout=workout)
    selected_exercises = {}
    for we in workout_exercises:
        muscle_name = we.exercise.muscle_group.name
        if muscle_name not in selected_exercises:
            selected_exercises[muscle_name] = []
        selected_exercises[muscle_name].append({
            'name': we.exercise.name,
            'sets': we.sets,
            'reps': we.reps
        })

    if request.method == 'POST':
        workout.name = request.POST.get('name', '').strip()
        workout.date = request.POST.get('date', '')
        workout.notes = request.POST.get('notes', '').strip() or None
        workout.save()

        WorkoutMuscleGroup.objects.filter(workout=workout).delete()
        WorkoutExercise.objects.filter(workout=workout).delete()

        selected_muscles = request.POST.getlist('muscle_groups')
        for muscle_name in selected_muscles:
            muscle_group = MuscleGroup.objects.filter(name=muscle_name).first()
            if muscle_group:
                WorkoutMuscleGroup.objects.create(workout=workout, muscle_group=muscle_group)

            selected_exercises_post = request.POST.getlist(f'exercises_{muscle_name}')
            for exercise_name in selected_exercises_post:
                exercise = Exercise.objects.filter(name=exercise_name).first()
                if exercise:
                    sets = request.POST.get(f'sets_{muscle_name}_{exercise_name}', '3')
                    reps = request.POST.get(f'reps_{muscle_name}_{exercise_name}', '8-10')
                    WorkoutExercise.objects.create(
                        workout=workout,
                        exercise=exercise,
                        sets=int(sets),
                        reps=reps
                    )

        messages.success(request, 'Workout updated successfully!')
        return redirect('workouts:workout_detail', workout_id=workout.id)

    return render(request, 'workouts/edit_workout.html', {
        'workout': workout,
        'muscle_groups': muscle_groups,
        'all_exercises': exercises_by_muscle,
        'selected_muscle_names': selected_muscle_names,
        'selected_exercises': selected_exercises
    })


@login_required
def delete_workout(request, workout_id):
    """
    Delete a workout and all associated muscle groups and exercises.
    Returns 404 if the workout does not belong to the logged-in user.
    """
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    WorkoutMuscleGroup.objects.filter(workout=workout).delete()
    WorkoutExercise.objects.filter(workout=workout).delete()
    workout.delete()
    messages.success(request, 'Workout deleted successfully!')
    return redirect('workouts:home')


@login_required
def stats(request):
    """
    Display workout statistics for the logged-in user.
    Calculates total workouts, most and least trained muscle groups,
    and number of completed goals.
    """
    from goals.models import Goal

    workouts = Workout.objects.filter(user=request.user)
    total_workouts = workouts.count()

    muscle_counts = {}
    for workout in workouts:
        for mg in workout.muscle_groups.all():
            muscle_counts[mg.name] = muscle_counts.get(mg.name, 0) + 1

    most_trained = max(muscle_counts, key=muscle_counts.get) if muscle_counts else 'N/A'
    least_trained = min(muscle_counts, key=muscle_counts.get) if muscle_counts else 'N/A'

    total_goals = Goal.objects.filter(user=request.user).count()
    completed_goals = Goal.objects.filter(user=request.user, is_completed=True).count()

    return render(request, 'workouts/stats.html', {
        'total_workouts': total_workouts,
        'most_trained': most_trained,
        'least_trained': least_trained,
        'muscle_stats': muscle_counts,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
    })


def about(request):
    """Display the about page with project information."""
    return render(request, 'workouts/about.html')