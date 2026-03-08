"""
fitbrigade_project/urls.py

URL configuration racine.
Les routes des apps seront ajoutées dans les prochaines sessions.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
