from django.contrib import admin
from .models import Bouquet, Cart, CartItem


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_editable = ('price', 'is_active')  # Можно редактировать прямо в списке
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')
    #prepopulated_fields = {'slug': ('name',)}  # Если добавите slug поле
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Дополнительно', {
            'fields': ('is_active', 'created_at'),
            'classes': ('collapse',)  # Сворачиваемый блок
        }),
    )
    readonly_fields = ('created_at',)  # Только для чтения


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price')
    list_select_related = ('user',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'total_price')

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Общая сумма'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('bouquet', 'cart', 'quantity', 'subtotal')
    list_filter = ('cart__user',)
    autocomplete_fields = ('bouquet', 'cart')  # Поиск при выборе

    def subtotal(self, obj):
        return obj.subtotal

    subtotal.short_description = 'Сумма'