from django.urls import path
from .views import CategoryListView, CategoryDetailView, PaymentViewSet, click_callback, payme_callback

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create'})),  # Ro‘yxat va yaratish
    path('payments/<int:pk>/', PaymentViewSet.as_view({'get': 'retrieve'})),  # Bitta to‘lovni olish
    path('payme/callback/', payme_callback, name='payme-callback'),  # Payme to‘lovni tasdiqlash
    path('click/callback/', click_callback, name='click-callback'),  # Click to‘lovni tasdiqlash

]
