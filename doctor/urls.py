from django.urls import path
from . import views

urlpatterns = [
    path('doctor_hisob/', views.doctor_hisob_list, name='doctor_hisob_list'),
    path('doctor_tajriba/', views.doctor_tajriba_list, name='doctor_tajriba_list'),
]
