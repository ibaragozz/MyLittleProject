from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm, UserProfileForm
from .models import UserProfile
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрированы! Пожалуйста, войдите.")
            return redirect('users:login')  # Исправлено на users:login
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('bouquets:home')
        else:
            messages.error(request, "Неверный логин или пароль.")
            return redirect('users:login')

    return render(request, 'users/login.html', {
        'register_url': reverse('users:register')
    })


@require_POST  # Разрешаем только POST-запросы
@never_cache  # Запрещаем кэширование
def logout_view(request):
    logout(request)
    return redirect('bouquets:home')


@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен")
            return redirect('users:profile')  # Добавлен namespace
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения сохранены")
            return redirect('users:profile')  # Исправлено на users:profile
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})