from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Bouquet, Cart, CartItem
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

def index(request):
    """Отображение каталога букетов"""
    bouquets = Bouquet.objects.filter(is_active=True)
    return render(request, 'bouquets/index.html', {
        'bouquets': bouquets,
        'title': 'Каталог букетов'
    })


@login_required
def add_to_cart(request, bouquet_id):
    """
    Добавление товара в корзину с использованием нового метода модели Cart
    """
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Используем новый метод add_item вместо прямого создания CartItem
    item, created = cart.add_item(bouquet)

    messages.success(
        request,
        f"'{bouquet.name}' {'добавлен в корзину' if created else 'уже есть в корзине (количество +1)'}"
    )
    return redirect('bouquets:catalog')


@login_required
def remove_from_cart(request, item_id):
    """
    Удаление товара из корзины
    """
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )
    bouquet_name = cart_item.bouquet.name
    cart_item.delete()

    messages.success(request, f"'{bouquet_name}' удален из корзины")
    return redirect('bouquets:view_cart')


@login_required
def update_cart_item(request, item_id):
    """
    Обновление количества товара через методы increase/decrease_quantity
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.increase_quantity()
            msg = "Количество увеличено"
        elif action == 'decrease':
            cart_item.decrease_quantity()
            msg = "Количество уменьшено"
        else:
            # Обработка прямого ввода количества
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                msg = "Количество обновлено"
            else:
                cart_item.delete()
                msg = "Товар удален"

        messages.success(request, msg)

    return redirect('bouquets:view_cart')


@login_required
def view_cart(request):
    """
    Просмотр корзины с автоматическим подсчетом суммы
    """
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'bouquets/cart.html', {
        'cart': cart,
        'title': 'Ваша корзина'
    })


@login_required
def clear_cart(request):
    """
    Очистка корзины через метод clear() модели Cart
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart.clear()  # Используем новый метод вместо items.all().delete()

    messages.success(request, "Корзина очищена")
    return redirect('bouquets:view_cart')

@login_required
def create_order(request):
    """Заглушка для страницы оформления заказа"""
    return render(request, 'bouquets/create_order.html', {
        'message': 'Форма оформления заказа будет здесь'
    })

@login_required
def order_detail(request, order_id):
    """
    Просмотр деталей конкретного заказа
    """
    order = get_object_or_404(
        Order,  # Убедитесь, что модель Order импортирована
        id=order_id,
        user=request.user  # Пользователь может видеть только свои заказы
    )
    return render(request, 'bouquets/order_detail.html', {
        'order': order,
        'title': f'Заказ #{order.id}'
    })