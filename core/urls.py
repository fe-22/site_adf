from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('loja/', views.loja, name='loja'),
    path('loja/produto/<int:pk>/', views.produto_detalhe, name='produto_detalhe'),
    path('agenda/', views.agenda, name='agenda'),
    path('galeria/', views.galeria, name='galeria'),
    path('parceiros/', views.parceiros, name='parceiros'),
    path('reunioes/', views.reunioes, name='reunioes'),
    path('oracao/', views.oracao, name='oracao'),
]
