from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text", "author"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "message", "author"]


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ["user", "comment"]


class MessageLikeForm(forms.ModelForm):
    class Meta:
        model = MessageLike
        fields = ["user", "message"]
