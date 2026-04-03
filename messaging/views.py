# messaging/views.py - à compléter dans les prochaines sessions
"""
messaging/views.py

Inbox system: send, receive, archive messages between users.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    """Display received messages for the logged-in user."""
    received = Message.objects.filter(
        recipient=request.user,
        is_archived=False
    )
    return render(request, 'messaging/inbox.html', {'messages_list': received})


@login_required
def sent_messages(request):
    """Display sent messages for the logged-in user."""
    sent = Message.objects.filter(sender=request.user)
    return render(request, 'messaging/sent_messages.html', {'messages_list': sent})


@login_required
def send_message(request):
    """Send a new message to another user."""
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()

        if not recipient_id or not subject or not body:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'messaging/send_message.html', {'users': users})

        recipient = get_object_or_404(User, id=recipient_id)
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        messages.success(request, f'Message sent to {recipient.username}!')
        return redirect('messaging:inbox')

    return render(request, 'messaging/send_message.html', {'users': users})


@login_required
def view_message(request, message_id):
    """View a single message and mark it as read."""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/view_message.html', {'message': message})


@login_required
def archive_message(request, message_id):
    """Archive a message."""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_archived = True
    message.save()
    messages.success(request, 'Message archived.')
    return redirect('messaging:inbox')