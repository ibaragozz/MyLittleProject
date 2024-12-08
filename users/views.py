from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Вы успешно зарегистрированы! Пожалуйста, войдите.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})  # Рендерим страницу с формой регистрации


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Редирект на главную страницу после входа

        else:
            # Логика для ошибки аутентификации
            messages.error(request, "Неверный логин или пароль.")
            return redirect('login')

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправление на главную страницу

@login_required
def profile_view(request):
    user = request.user  # Получаем текущего пользователя
    return render(request, 'users/profile.html', {'user': user})