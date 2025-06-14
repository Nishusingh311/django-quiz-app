from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Signup Form
class SignUpForm( forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("Confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

#Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput)