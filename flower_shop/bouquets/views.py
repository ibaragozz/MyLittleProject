from django.shortcuts import render
from .models import Bouquet

def index(request):
    bouquets = Bouquet.objects.all()  # Получаем все букеты из базы данных
    return render(request, 'bouquets/index.html', {'bouquets': bouquets})  # Передаем букеты в шаблон
