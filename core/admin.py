from django.contrib import admin
from .models import Produto, Evento, FotoCulto, Empresa

admin.site.site_header = 'ADFidelidade Central - Administração'
admin.site.site_title = 'ADFidelidade'
admin.site.index_title = 'Painel Administrativo'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'disponivel', 'criado_em']
    list_filter = ['categoria', 'disponivel']
    search_fields = ['nome', 'descricao']
    list_editable = ['disponivel', 'preco']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'data', 'hora', 'local', 'recorrente']
    list_filter = ['tipo', 'recorrente', 'data']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data'


@admin.register(FotoCulto)
class FotoCultoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_culto', 'destaque', 'criado_em']
    list_filter = ['destaque', 'data_culto']
    search_fields = ['titulo', 'descricao']
    list_editable = ['destaque']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'site', 'ativo', 'criado_em']
    list_filter = ['ativo']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo']
