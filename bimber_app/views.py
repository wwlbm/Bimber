from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileEditForm
from .models import CustomUser, Message


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    is_editing = request.GET.get('edit') == '1'

    if request.method == 'POST' and is_editing:
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'profile.html', {
        'form': form,
        'is_editing': is_editing
    })

@login_required
def discover_view(request):
    user = request.user

    if user.gender == 'M':
        search_gender = 'F'
    elif user.gender == 'F':
        search_gender = 'M'
    else:
        messages.warning(request, 'Please enter your gender in your profile to get started.')
        return redirect('profile')

    potential_matches = CustomUser.objects.filter(
        gender=search_gender
    ).exclude(id=user.id).order_by('?')

    return render(request, 'discover.html', {'potential_matches': potential_matches})