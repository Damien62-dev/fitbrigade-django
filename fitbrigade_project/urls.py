from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('', include('workouts.urls', namespace='workouts')),
    path('goals/', include('goals.urls', namespace='goals')),
]