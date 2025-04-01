from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
from .models import Bouquet, Cart, CartItem, Order, OrderItem
from .forms import OrderForm
from django.db import transaction

def index(request):
    """Отображение каталога букетов"""
    bouquets = Bouquet.objects.filter(is_active=True)
    return render(request, 'bouquets/index.html', {
        'bouquets': bouquets,
        'user': request.user
    })


@login_required
def add_to_cart(request, bouquet_id):
    """Добавление товара в корзину"""
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = cart.add_item(bouquet)

    messages.success(
        request,
        f"'{bouquet.name}' {'добавлен в корзину' if created else 'уже есть в корзине (количество +1)'}"
    )
    return redirect('bouquets:catalog')


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
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
    """Обновление количества товара"""
    if request.method == 'POST':
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', cart_item.quantity))

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                messages.success(request, "Товар удалён из корзины")
                return redirect('bouquets:view_cart')
        else:
            if quantity >= 1:
                cart_item.quantity = quantity
            else:
                cart_item.delete()
                messages.success(request, "Товар удалён из корзины")
                return redirect('bouquets:view_cart')

        cart_item.save()
        messages.success(request, "Количество обновлено")

    return redirect('bouquets:view_cart')


@login_required
def view_cart(request):
    """Просмотр корзины"""
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'bouquets/cart.html', {
        'cart': cart,
        'title': 'Ваша корзина'
    })


@login_required
def clear_cart(request):
    """Очистка корзины"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.clear()
    messages.success(request, "Корзина очищена")
    return redirect('bouquets:view_cart')


def send_telegram_notification(order):
    """Отправка уведомления в Telegram"""
    try:
        items_text = "\n".join(
            f"• {item.bouquet.name} × {item.quantity} = {item.price * item.quantity}₽"
            for item in order.items.all()
        )

        message = (
            f"🛍 *Новый заказ #{order.id}*\n"
            f"👤 Клиент: {order.user.username}\n"
            f"📞 Телефон: {order.phone}\n"
            f"🏠 Адрес: {order.delivery_address}\n"
            f"💐 Состав:\n{items_text}\n"
            f"💵 Итого: {order.total_price}₽\n"
            f"📝 Комментарий: {order.comment or 'нет'}"
        )
        print(f"\n=== Тестовое сообщение для Telegram ===\n{message}\n=====================\n")
        response = requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                'chat_id': settings.TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            },
            timeout=5
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


@login_required
def create_order(request):
    """Оформление заказа с отправкой в Telegram"""
    cart = get_object_or_404(Cart, user=request.user)

    print("\n=== 1. Начало создания заказа ===")

    if not cart.items.exists():
        messages.error(request, "Корзина пуста!")
        return redirect('bouquets:view_cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                print("=== 2. Форма валидна ===")

                with transaction.atomic():
                    # Создаем заказ
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = cart.total_price
                    order.save()

                    print(f"=== 3. Заказ #{order.id} создан ===")

                    # Переносим товары
                    for item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            bouquet=item.bouquet,
                            quantity=item.quantity,
                            price=item.bouquet.price
                        )

                    print("=== 4. Товары перенесены ===")
                    # Отправляем в Telegram
                    if not send_telegram_notification(order):
                        messages.warning(request, "Заказ создан, но не отправлен в Telegram")

                    telegram_result = send_telegram_notification(order)
                    print(f"=== 5. Результат отправки в Telegram: {telegram_result} ===")

                    # Очищаем корзину
                    cart.clear()

                    messages.success(request, f"Заказ #{order.id} оформлен! Проверьте Telegram.")
                    return redirect('bouquets:order_detail', order_id=order.id)

            except Exception as e:
                print(f"=== ОШИБКА: {str(e)} ===")
                messages.error(request, f"Ошибка оформления заказа: {str(e)}")
                return redirect('bouquets:view_cart')
    else:
        form = OrderForm()

    return render(request, 'bouquets/create_order.html', {
        'form': form,
        'cart': cart
    })


@login_required
def order_detail(request, order_id):
    """Просмотр деталей заказа"""
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )
    return render(request, 'bouquets/order_detail.html', {
        'order': order,
        'title': f'Заказ #{order.id}'
    })