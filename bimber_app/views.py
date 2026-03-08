from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileEditForm
from .models import CustomUser, Message, Match


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

    viewed_ids = Match.objects.filter(from_user=user).values_list('to_user_id', flat=True)

    if user.gender == 'M':
        search_gender = 'F'
    elif user.gender == 'F':
        search_gender = 'M'
    else:
        messages.warning(request, 'Please enter your gender in your profile to get started.')
        return redirect('profile')

    if not user.city:
        messages.warning(request, 'Please enter your city in your profile to get started.')
        return redirect('profile')

    if not user.age:
        messages.warning(request, 'Please enter your age in your profile to get started.')
        return redirect('profile')

    min_age = user.age - 5
    max_age = user.age + 5

    potential_matches = CustomUser.objects.filter(
        gender=search_gender,
        city=user.city,
        age__gte=min_age,
        age__lte=max_age
    ).exclude(id=user.id).exclude(id__in=viewed_ids).order_by('?')

    return render(request, 'discover.html', {'potential_matches': potential_matches})


@login_required
def inbox_view(request):
    messages_list = request.user.received_messages.all()
    messages_list.update(is_read=True)

    return render(request, 'inbox.html', {'messages': messages_list})

@login_required
def rate_user(request, user_id, action):
    target_user = get_object_or_404(CustomUser, id=user_id)
    is_like = (action == 'like')

    Match.objects.get_or_create(
        from_user=request.user,
        to_user=target_user,
        defaults={'is_like': is_like}
    )

    if is_like:
        Message.objects.create(
            sender=request.user,
            recipient=target_user,
            message=f"User {request.user.username} liked you"
        )

    return redirect('discover')

@login_required
def view_profile(request, user_id):
    person = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'view_profile.html', {'person': person})