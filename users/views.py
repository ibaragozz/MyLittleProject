from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            messages.success(request, "Вы успешно зарегистрированы! Пожалуйста, войдите.")  # Сообщение об успешной регистрации
            return redirect('home')  # Редирект на главную страницу после регистрации
    else:
        form = RegisterForm()  # Если это GET-запрос, показываем пустую форму

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
