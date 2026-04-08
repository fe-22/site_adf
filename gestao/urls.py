from django.urls import path
from . import views

app_name = 'gestao'

urlpatterns = [
    # Auth
    path('login/', views.painel_login, name='login'),
    path('logout/', views.painel_logout, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Reuniões Gerais
    path('reunioes/', views.reuniao_lista, name='reuniao_lista'),
    path('reunioes/nova/', views.reuniao_criar, name='reuniao_criar'),
    path('reunioes/<int:pk>/editar/', views.reuniao_editar, name='reuniao_editar'),
    path('reunioes/<int:pk>/deletar/', views.reuniao_deletar, name='reuniao_deletar'),
    path('reunioes/<int:pk>/qrcode/', views.reuniao_qrcode, name='reuniao_qrcode'),
    path('reunioes/<int:pk>/presencas/', views.reuniao_presencas, name='reuniao_presencas'),
    path('reunioes/<int:pk>/presencas/export/', views.reuniao_presencas_export, name='reuniao_presencas_export'),

    # Reuniões de Obreiros
    path('obreiros/', views.reuniao_obreiros_lista, name='reuniao_obreiros_lista'),

    # Presença pública (via QR code) — sem login required
    path('presenca/<int:pk>/', views.presenca_publica, name='presenca_publica'),

    # Galeria
    path('galeria/', views.foto_lista, name='foto_lista'),
    path('galeria/upload/', views.foto_upload, name='foto_upload'),
    path('galeria/<int:pk>/editar/', views.foto_editar, name='foto_editar'),
    path('galeria/<int:pk>/deletar/', views.foto_deletar, name='foto_deletar'),

    # Loja
    path('loja/', views.produto_lista, name='produto_lista'),
    path('loja/novo/', views.produto_criar, name='produto_criar'),
    path('loja/<int:pk>/editar/', views.produto_editar, name='produto_editar'),
    path('loja/<int:pk>/deletar/', views.produto_deletar, name='produto_deletar'),

    # Agenda
    path('agenda/', views.evento_lista, name='evento_lista'),
    path('agenda/novo/', views.evento_criar, name='evento_criar'),
    path('agenda/<int:pk>/editar/', views.evento_editar, name='evento_editar'),
    path('agenda/<int:pk>/deletar/', views.evento_deletar, name='evento_deletar'),

    # Parceiros
    path('parceiros/', views.parceiro_lista, name='parceiro_lista'),
    path('parceiros/novo/', views.parceiro_criar, name='parceiro_criar'),
    path('parceiros/<int:pk>/editar/', views.parceiro_editar, name='parceiro_editar'),
    path('parceiros/<int:pk>/deletar/', views.parceiro_deletar, name='parceiro_deletar'),

    # Novos Membros (painel)
    path('membros/', views.membro_lista, name='membro_lista'),
    path('membros/<int:pk>/atender/', views.membro_atender, name='membro_atender'),
    path('membros/<int:pk>/deletar/', views.membro_deletar, name='membro_deletar'),

    # Formulário público de novos membros
    path('novo-membro/', views.novo_membro_form, name='novo_membro_form'),

    # Vigília / Consagração de Oração
    path('vigilia/', views.vigilia_lista, name='vigilia_lista'),
    path('vigilia/nova/', views.vigilia_criar, name='vigilia_criar'),
    path('vigilia/<int:pk>/editar/', views.vigilia_editar, name='vigilia_editar'),
    path('vigilia/<int:pk>/deletar/', views.vigilia_deletar, name='vigilia_deletar'),
    path('vigilia/<int:pk>/horarios/', views.vigilia_horarios, name='vigilia_horarios'),
    path('vigilia/inscricao/<int:pk>/remover/', views.vigilia_remover_inscricao, name='vigilia_remover_inscricao'),
]
