from django.contrib import admin
from .models import Bouquet

# Регистрация модели Bouquet в админке
@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')  # Отображение полей в списке
    search_fields = ('name',)  # Поле для поиска по названию
    list_filter = ('price', 'created_at')  # Фильтры