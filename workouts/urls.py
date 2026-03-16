from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.home, name='home'),
    path('workout/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('create/', views.create_workout, name='create_workout'),
    path('edit/<int:workout_id>/', views.edit_workout, name='edit_workout'),
    path('delete/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('stats/', views.stats, name='stats'),
    path('about/', views.about, name='about'),
]