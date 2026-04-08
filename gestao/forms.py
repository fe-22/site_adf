from django import forms
from .models import Reuniao, Presenca, NovoMembro, ConsagracaoOracao
from core.models import FotoCulto, Produto, Evento, Empresa


class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = Reuniao
        fields = ['tipo', 'titulo', 'descricao', 'data', 'hora', 'local']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class PresencaPublicaForm(forms.ModelForm):
    class Meta:
        model = Presenca
        fields = ['nome', 'telefone']


class FotoCultoForm(forms.ModelForm):
    class Meta:
        model = FotoCulto
        fields = ['titulo', 'descricao', 'imagem', 'data_culto', 'destaque']
        widgets = {
            'data_culto': forms.DateInput(attrs={'type': 'date'}),
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'categoria', 'imagem', 'disponivel']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'tipo', 'data', 'hora', 'local', 'recorrente']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'descricao', 'logo', 'site', 'telefone', 'instagram', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class NovoMembroForm(forms.ModelForm):
    class Meta:
        model = NovoMembro
        fields = ['nome', 'email', 'telefone', 'data_nascimento', 'endereco', 'como_conheceu', 'observacoes']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Deixe aqui qualquer mensagem, pedido de oração ou comentário...'}),
        }


class ConsagracaoOracaoForm(forms.ModelForm):
    class Meta:
        model = ConsagracaoOracao
        fields = ['titulo', 'descricao', 'data_inicio', 'data_fim', 'ativa']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Mensagem de convocação para a igreja...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['data_fim'].input_formats = ['%Y-%m-%dT%H:%M']


class InscricaoOracaoForm(forms.Form):
    nome = forms.CharField(
        max_length=200, label='Seu Nome Completo',
        widget=forms.TextInput(attrs={'placeholder': 'Nome do obreiro(a)'}),
    )
    telefone = forms.CharField(
        max_length=20, required=False, label='Telefone / WhatsApp (opcional)',
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
    )
    hora_inicio = forms.CharField(widget=forms.HiddenInput())
