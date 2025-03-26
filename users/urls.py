from django.urls import path
from . import views

app_name = 'users'  # Добавляем пространство имен

urlpatterns = [
    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Профиль
    path('profile/', views.profile_view, name='profile'),

    # API (опционально)
    # path('api/profile/', views.profile_api, name='profile_api'),
]