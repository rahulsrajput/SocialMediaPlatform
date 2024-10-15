from django import forms
# from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name']


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username']