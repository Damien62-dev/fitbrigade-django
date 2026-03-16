from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal
from workouts.models import Exercise, MuscleGroup


@login_required
def goals_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals/goals.html', {'goals': goals})


@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    return render(request, 'goals/goal_detail.html', {'goal': goal})


@login_required
def create_goal(request):
    muscle_groups = MuscleGroup.objects.all()
    exercises_by_muscle = {}
    for mg in muscle_groups:
        exercises_by_muscle[mg.name] = Exercise.objects.filter(muscle_group=mg)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        notes = request.POST.get('notes', '').strip()

        if not name or not notes:
            messages.error(request, 'Please fill in goal name and description.')
            return render(request, 'goals/create_goal.html', {
                'muscle_groups': muscle_groups,
                'all_exercises': exercises_by_muscle
            })

        deadline_str = request.POST.get('deadline', '').strip()
        exercise_id = request.POST.get('exercise', '').strip()
        target_weight = request.POST.get('target_weight', '').strip()
        target_reps = request.POST.get('target_reps', '').strip()

        goal = Goal.objects.create(
            user=request.user,
            name=name,
            notes=notes,
            deadline=deadline_str if deadline_str else None,
            exercise_id=int(exercise_id) if exercise_id else None,
            target_weight=float(target_weight) if target_weight else None,
            target_reps=int(target_reps) if target_reps else None,
        )

        messages.success(request, 'Goal created successfully!')
        return redirect('goals:goals_list')

    return render(request, 'goals/create_goal.html', {
        'muscle_groups': muscle_groups,
        'all_exercises': exercises_by_muscle
    })


@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    muscle_groups = MuscleGroup.objects.all()
    exercises_by_muscle = {}
    for mg in muscle_groups:
        exercises_by_muscle[mg.name] = Exercise.objects.filter(muscle_group=mg)

    if request.method == 'POST':
        goal.name = request.POST.get('name', '').strip()
        goal.notes = request.POST.get('notes', '').strip()
        deadline_str = request.POST.get('deadline', '').strip()
        exercise_id = request.POST.get('exercise', '').strip()
        target_weight = request.POST.get('target_weight', '').strip()
        target_reps = request.POST.get('target_reps', '').strip()

        goal.deadline = deadline_str if deadline_str else None
        goal.exercise_id = int(exercise_id) if exercise_id else None
        goal.target_weight = float(target_weight) if target_weight else None
        goal.target_reps = int(target_reps) if target_reps else None
        goal.save()

        messages.success(request, 'Goal updated successfully!')
        return redirect('goals:goal_detail', goal_id=goal.id)

    return render(request, 'goals/edit_goal.html', {
        'goal': goal,
        'muscle_groups': muscle_groups,
        'all_exercises': exercises_by_muscle
    })


@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.delete()
    messages.success(request, 'Goal deleted successfully!')
    return redirect('goals:goals_list')