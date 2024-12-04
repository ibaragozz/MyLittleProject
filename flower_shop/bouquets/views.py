from django.shortcuts import render
from .models import Bouquet

def index(request):
    bouquets = Bouquet.objects.all()
    return render(request, 'index.html', {'bouquets': bouquets})