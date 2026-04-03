# messaging/urls.py - à compléter dans les prochaines sessions
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('send/', views.send_message, name='send_message'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('archive/<int:message_id>/', views.archive_message, name='archive_message'),
]