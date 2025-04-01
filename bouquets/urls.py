from django.urls import path
from . import views

app_name = 'bouquets'

urlpatterns = [
    # Основные маршруты
    path('', views.index, name='home'),
    path('catalog/', views.index, name='catalog'),
    path('cart/', views.view_cart, name='view_cart'),

    # Маршруты корзины
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:bouquet_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    path('test-order/', views.test_order, name='test_order'), # Временный тестовый URL
    # Маршруты для API (опционально)
    # path('api/cart/', views.cart_api, name='cart_api'),
    # path('api/cart/add/', views.add_to_cart_api, name='add_to_cart_api'),
]