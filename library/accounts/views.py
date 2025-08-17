from django.shortcuts import render
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have regstered successfully")
            redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.userprofile  # thanks to signals, profile exists
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form})