from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estoque/', views.estoque, name='estoque'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('vendas/',views.vendas, name='vendas'),
]
