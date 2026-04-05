from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goals_list, name='goals_list'),
    path('<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('create/', views.create_goal, name='create_goal'),
    path('edit/<int:goal_id>/', views.edit_goal, name='edit_goal'),
    path('delete/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('complete/<int:goal_id>/', views.complete_goal, name='complete_goal'),
]