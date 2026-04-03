document.addEventListener('DOMContentLoaded', function () {

    // update the muscle group counter display
    function updateMuscleCount() {
        const selectedBoxes = document.querySelectorAll('input[name="muscle_groups"]:checked');
        const totalCount = selectedBoxes.length;
        const counterElement = document.getElementById('muscleCount');
        if (counterElement) {
            let displayText = '';
            if (totalCount === 1) {
                displayText = totalCount + ' muscle group selected';
            } else {
                displayText = totalCount + ' muscle groups selected';
            }
            counterElement.textContent = displayText;
        }
    }

    // show or hide exercise details
    function toggleExerciseDetails(muscle, exercise, event) {
        const checkbox = event.target;
        const divId = 'details_' + muscle + '_' + exercise;
        const detailsDiv = document.getElementById(divId);
        if (checkbox.checked) {
            detailsDiv.style.display = 'flex';
        } else {
            detailsDiv.style.display = 'none';
        }
    }

    // toggle exercise section when muscle group is selected
    function toggleExercises(muscle, event) {
        const checkbox = event.target;
        const sectionId = 'exercises_' + muscle;
        const exerciseSection = document.getElementById(sectionId);
        if (checkbox.checked === true) {
            exerciseSection.style.display = 'block';
        } else {
            exerciseSection.style.display = 'none';
            const allCheckboxes = exerciseSection.querySelectorAll('input[type="checkbox"]');
            for (let i = 0; i < allCheckboxes.length; i = i + 1) {
                allCheckboxes[i].checked = false;
            }
        }
        updateMuscleCount();
    }

    // Expose functions globally so inline onchange= handlers can call them
    window.toggleExercises = toggleExercises;
    window.toggleExerciseDetails = toggleExerciseDetails;

    // Confirm before deleting a workout
    const deleteWorkoutLinks = document.querySelectorAll('a[href*="/delete/"]');
    deleteWorkoutLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this workout? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });

    // Confirm before deleting a goal
    const deleteGoalLinks = document.querySelectorAll('a[href*="/goals/"][href*="/delete/"]');
    deleteGoalLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this goal? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });

    // Pre-populate edit workout form (only runs if the data element exists)
    const editWorkoutData = document.getElementById('selectedExercisesData');
    if (editWorkoutData) {
        const selectedExercises = JSON.parse(editWorkoutData.textContent);
        for (const [muscle, exercises] of Object.entries(selectedExercises)) {
            for (const ex of exercises) {
                const chk = document.getElementById('chk_' + muscle + '_' + ex.name);
                if (chk) {
                    chk.checked = true;
                    const details = document.getElementById('details_' + muscle + '_' + ex.name);
                    if (details) {
                        details.style.display = 'flex';
                        const setsSelect = details.querySelector('select[name="sets_' + muscle + '_' + ex.name + '"]');
                        const repsSelect = details.querySelector('select[name="reps_' + muscle + '_' + ex.name + '"]');
                        if (setsSelect) setsSelect.value = ex.sets;
                        if (repsSelect) repsSelect.value = ex.reps;
                    }
                }
            }
        }
    }

    // ===== Auto-dismiss toasts après 3 secondes =====
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            const bsToast = bootstrap.Toast.getOrCreateInstance(toast);
            bsToast.hide();
        }, 3000);
    });
});