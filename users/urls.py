from django.urls import path
from . import views

app_name = 'users'  # Добавляем пространство имен

urlpatterns = [
    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # API (опционально)
    # path('api/profile/', views.profile_api, name='profile_api'),
]