from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Главная страница с именем 'home'
    # Другие маршруты
]
