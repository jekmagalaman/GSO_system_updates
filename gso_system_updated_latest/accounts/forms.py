from django import forms
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'unit', 'department', 'role', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        role = self.instance.role if self.instance else None

        if role == "requestor":
            self.fields['first_name'].required = False
            self.fields['last_name'].required = False
            self.fields['unit'].required = False
        elif role == "gso":
            self.fields['unit'].required = False
            self.fields['department'].required = False
        else:  # unit_head or personnel
            self.fields['department'].required = False








class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "role", "unit", 
            "first_name", "last_name", "department",
            "username", "email", "is_active", "password"
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        if role == "employee":
            cleaned_data["first_name"] = ""
            cleaned_data["last_name"] = ""
        return cleaned_data
    



















class RequestorProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "role", "unit"]