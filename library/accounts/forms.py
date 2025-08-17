from django.contrib.auth.forms import UserCreationForm 
from .models import CustomUser, UserProfile
from django import forms 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser 
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']