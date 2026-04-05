"""
users/forms.py

Forms for user registration, profile update, and profile picture update.
Uses Django Crispy Forms for Bootstrap 5 styling.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import CustomUser, Profile


class UserRegisterForm(UserCreationForm):
    """
    Form for new user registration.
    Extends Django's UserCreationForm with an email field.
    Styled with Crispy Forms Bootstrap 5.
    """
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign Up'))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user account information.
    Allows editing of username, email, and personal contact details.
    Styled with Crispy Forms Bootstrap 5.
    """
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Update Profile'))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'bio']


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the user's profile picture.
    Images are automatically resized to 300x300px on save via the Profile model.
    """
    class Meta:
        model = Profile
        fields = ['image']