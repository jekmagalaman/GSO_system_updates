from django import forms
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'unit', 'role', 'is_active']  # Adjust to your model


class RequestorProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "role", "unit"]