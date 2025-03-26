from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Bouquet, Cart, CartItem
from django.contrib.auth.decorators import login_required


def index(request):
    bouquets = Bouquet.objects.filter(is_active=True)  # Только активные букеты
    return render(request, 'bouquets/index.html', {'bouquets': bouquets})


@login_required
def add_to_cart(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Получаем или создаем элемент корзины
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        bouquet=bouquet,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Количество '{bouquet.name}' обновлено в корзине")
    else:
        messages.success(request, f"'{bouquet.name}' добавлен в корзину")

    return redirect('bouquets:catalog')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    bouquet_name = cart_item.bouquet.name
    cart_item.delete()
    messages.success(request, f"'{bouquet_name}' удален из корзины")
    return redirect('bouquets:view_cart')


@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Количество обновлено")
        else:
            cart_item.delete()
            messages.success(request, "Товар удален из корзины")

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'bouquets/cart.html', {'cart': cart})


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, "Корзина очищена")
    return redirect('view_cart')