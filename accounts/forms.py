from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'name']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'phone']

class ThemeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['theme']
