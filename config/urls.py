from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# Swagger konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="Onlayn Tabib API",
        default_version='v1',
        description="Onlayn Tabib ilovasining API hujjatlari",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@onlayntabib.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('register/', include('register.urls')),  # Foydalanuvchi ro‘yxatdan o‘tishi
    path('user/', include('user.urls')),  # User ilovasi
    path('doctor/', include('doctor.urls')),  # Doctor ilovasi

    # Swagger API dokumentatsiyasi
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# DEBUG rejimida statik va media fayllarni qo‘shish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# I18n (Ko‘p tillik) URL'larni qo‘shish
urlpatterns += i18n_patterns(
    path('language/', include('register.urls')),  # Tilni o‘zgartirish uchun
    prefix_default_language=False,
)
