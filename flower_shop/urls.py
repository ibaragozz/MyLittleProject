from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # Добавьте этот импорт

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bouquets.urls', namespace='bouquets')),  # Явно указываем namespace
    path('users/', include('users.urls', namespace='users')),

    # Добавьте fallback-редирект для админки
    path('', RedirectView.as_view(url='bouquets/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)