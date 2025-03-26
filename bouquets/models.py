from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Bouquet(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название букета'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True  # Делаем необязательным
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)]  # Цена не может быть отрицательной
    )
    image = models.ImageField(
        upload_to='bouquets/',
        verbose_name='Изображение'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный товар'
    )

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'
        ordering = ['-created_at']  # Сортировка по дате (новые сначала)

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.CASCADE,
        verbose_name='Букет'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = [['cart', 'bouquet']]  # Уникальная пара корзина-букет

    def __str__(self):
        return f"{self.bouquet.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.bouquet.price * self.quantity