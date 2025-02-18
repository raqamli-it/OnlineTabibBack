from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from config import settings
from django.conf.urls.static import static

# Swagger konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="Onlayn Tabib API",  # API nomini o'zgartirdim
        default_version='v1',
        description="Onlayn Tabib ilovasining API hujjatlari",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@onlayntabib.local"),  # Kontaktni o'zgartirdim
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('register/', include('register.urls')),  # register app URL'larini ulash
    path('user/',include('user.urls')),
    path('doctor/',include('doctor.urls')),
    # Swagger dokumentatsiyasi
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#urlpatterns += i18n_patterns(
    #path('language', include('register.urls')),
    #prefix_default_language=False,
#)