"""
messaging/views.py

Inbox system: send, receive, and archive messages between users.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    """
    Display the inbox for the logged-in user.
    Shows all received messages that have not been archived.
    """
    received = Message.objects.filter(
        recipient=request.user,
        is_archived=False
    )
    return render(request, 'messaging/inbox.html', {'messages_list': received})


@login_required
def sent_messages(request):
    """
    Display all messages sent by the logged-in user.
    Ordered by most recent first.
    """
    sent = Message.objects.filter(sender=request.user)
    return render(request, 'messaging/sent_messages.html', {'messages_list': sent})


@login_required
def send_message(request):
    """
    Handle sending a new message to another user.
    GET: Display the message composition form with a list of available recipients.
    POST: Validate and save the message, then redirect to inbox.
    """
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
    """
    Display a single message and mark it as read.
    Automatically sets is_read to True on first view.
    Returns 404 if the message does not belong to the logged-in user.
    """
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/view_message.html', {'message': message})


@login_required
def archive_message(request, message_id):
    """
    Archive a message by setting is_archived to True.
    Archived messages are hidden from the main inbox.
    Returns 404 if the message does not belong to the logged-in user.
    """
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_archived = True
    message.save()
    messages.success(request, 'Message archived.')
    return redirect('messaging:inbox')