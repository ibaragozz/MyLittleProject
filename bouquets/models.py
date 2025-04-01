from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Bouquet(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название букета')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='bouquets/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активный товар')

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('bouquets:bouquet_detail', args=[str(self.id)])

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def add_item(self, bouquet):
        """
        Добавляет товар в корзину или увеличивает количество, если товар уже есть.
        Возвращает (CartItem, created), где created — True, если товар был добавлен впервые.
        """
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            bouquet=bouquet,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return cart_item, created

    def clear(self):
        """Очищает корзину"""
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name}"

    @property
    def subtotal(self):
        return self.bouquet.price * self.quantity

class Order(models.Model):
    STATUSES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменен')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'  # Добавлено
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'  # Добавлено
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'  # Новое поле
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='new',
        verbose_name='Статус'  # Добавлено
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая сумма'  # Добавлено
    )
    delivery_address = models.TextField(
        verbose_name='Адрес доставки'  # Добавлено
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'  # Добавлено
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'  # Добавлено
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ #{self.id} ({self.get_status_display()})"

    @property
    def items_count(self):
        """Общее количество товаров в заказе"""
        return self.items.count()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'  # Добавлено
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.PROTECT,
        verbose_name='Букет'  # Добавлено
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'  # Добавлено
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена за единицу'  # Добавлено
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.bouquet.name} x{self.quantity}"

    @property
    def subtotal(self):
        """Сумма по позиции"""
        return self.price * self.quantity