import io
import csv
import base64
import qrcode
import qrcode.constants

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError

from .models import Reuniao, Presenca, NovoMembro, ConsagracaoOracao, HorarioOracao
from .forms import (
    ReuniaoForm, PresencaPublicaForm, FotoCultoForm,
    ProdutoForm, EventoForm, EmpresaForm, NovoMembroForm,
    ConsagracaoOracaoForm, InscricaoOracaoForm,
)
from core.models import FotoCulto, Produto, Evento, Empresa


# ─── AUTENTICAÇÃO ────────────────────────────────────────────────────────────

def painel_login(request):
    if request.user.is_authenticated:
        return redirect('gestao:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('gestao:dashboard')
        messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'gestao/login.html')


def painel_logout(request):
    logout(request)
    return redirect('gestao:login')


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    from django.utils import timezone
    now = timezone.now()
    context = {
        'total_eventos': Evento.objects.count(),
        'total_fotos': FotoCulto.objects.count(),
        'total_produtos': Produto.objects.count(),
        'total_parceiros': Empresa.objects.filter(ativo=True).count(),
        'total_reunioes': Reuniao.objects.filter(tipo='geral').count(),
        'total_obreiros': Reuniao.objects.filter(tipo='obreiros').count(),
        'total_membros_pendentes': NovoMembro.objects.filter(atendido=False).count(),
        'reunioes_recentes': Reuniao.objects.order_by('-criado_em')[:5],
        'vigilia_ativa': ConsagracaoOracao.objects.filter(ativa=True, data_fim__gte=now).order_by('data_inicio').first(),
    }
    return render(request, 'gestao/dashboard.html', context)


# ─── REUNIÕES ────────────────────────────────────────────────────────────────

@login_required
def reuniao_lista(request):
    reunioes = Reuniao.objects.filter(tipo='geral')
    return render(request, 'gestao/reuniao_lista.html', {
        'reunioes': reunioes,
        'tipo': 'geral',
        'titulo_lista': 'Reuniões Gerais',
        'criar_url': reverse('gestao:reuniao_criar') + '?tipo=geral',
    })


@login_required
def reuniao_obreiros_lista(request):
    reunioes = Reuniao.objects.filter(tipo='obreiros')
    return render(request, 'gestao/reuniao_lista.html', {
        'reunioes': reunioes,
        'tipo': 'obreiros',
        'titulo_lista': 'Reuniões de Obreiros',
        'criar_url': reverse('gestao:reuniao_criar') + '?tipo=obreiros',
    })


@login_required
def reuniao_criar(request):
    tipo = request.GET.get('tipo', 'geral')
    if tipo not in ['geral', 'obreiros']:
        tipo = 'geral'
    form = ReuniaoForm(request.POST or None, initial={'tipo': tipo})
    if form.is_valid():
        reuniao = form.save()
        messages.success(request, 'Reunião agendada com sucesso!')
        if reuniao.tipo == 'obreiros':
            return redirect('gestao:reuniao_obreiros_lista')
        return redirect('gestao:reuniao_lista')
    back_url = reverse('gestao:reuniao_obreiros_lista') if tipo == 'obreiros' else reverse('gestao:reuniao_lista')
    titulo = 'Nova Reunião de Obreiros' if tipo == 'obreiros' else 'Nova Reunião'
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': titulo,
        'back_url': back_url,
    })


@login_required
def reuniao_editar(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    form = ReuniaoForm(request.POST or None, instance=reuniao)
    if form.is_valid():
        saved = form.save()
        messages.success(request, 'Reunião atualizada!')
        if saved.tipo == 'obreiros':
            return redirect('gestao:reuniao_obreiros_lista')
        return redirect('gestao:reuniao_lista')
    back_url = reverse('gestao:reuniao_obreiros_lista') if reuniao.tipo == 'obreiros' else reverse('gestao:reuniao_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Editar Reunião',
        'objeto': str(reuniao),
        'back_url': back_url,
    })


@login_required
@require_POST
def reuniao_deletar(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    tipo = reuniao.tipo
    reuniao.delete()
    messages.success(request, 'Reunião removida.')
    if tipo == 'obreiros':
        return redirect('gestao:reuniao_obreiros_lista')
    return redirect('gestao:reuniao_lista')


@login_required
def reuniao_qrcode(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    url = request.build_absolute_uri(reverse('gestao:presenca_publica', args=[pk]))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#2e3d0f', back_color='white')

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'gestao/reuniao_qrcode.html', {
        'reuniao': reuniao,
        'qr_code': qr_b64,
        'url': url,
        'total_presencas': reuniao.presencas.count(),
    })


@login_required
def reuniao_presencas(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    presencas = reuniao.presencas.order_by('nome')
    return render(request, 'gestao/reuniao_presencas.html', {
        'reuniao': reuniao,
        'presencas': presencas,
    })


@login_required
def reuniao_presencas_export(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    presencas = reuniao.presencas.order_by('nome')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="presencas_{reuniao.pk}.csv"'
    response.write('\ufeff')  # BOM para Excel reconhecer UTF-8

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Telefone', 'Registrado em'])
    for p in presencas:
        writer.writerow([p.nome, p.telefone, p.registrado_em.strftime('%d/%m/%Y %H:%M')])
    return response


# ─── PRESENÇA PÚBLICA (via QR code) ──────────────────────────────────────────

def presenca_publica(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)
    form = PresencaPublicaForm(request.POST or None)
    confirmado = False

    if request.method == 'POST' and form.is_valid():
        presenca = form.save(commit=False)
        presenca.reuniao = reuniao
        try:
            presenca.save()
            confirmado = True
        except IntegrityError:
            form.add_error('nome', 'Este nome já foi registrado nesta reunião.')

    return render(request, 'gestao/presenca_publica.html', {
        'reuniao': reuniao,
        'form': form,
        'confirmado': confirmado,
    })


# ─── GALERIA ─────────────────────────────────────────────────────────────────

@login_required
def foto_lista(request):
    fotos = FotoCulto.objects.all()
    return render(request, 'gestao/foto_lista.html', {'fotos': fotos})


@login_required
def foto_upload(request):
    form = FotoCultoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Foto adicionada à galeria!')
        return redirect('gestao:foto_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Upload de Foto',
        'back_url': reverse('gestao:foto_lista'),
        'multipart': True,
    })


@login_required
def foto_editar(request, pk):
    foto = get_object_or_404(FotoCulto, pk=pk)
    form = FotoCultoForm(request.POST or None, request.FILES or None, instance=foto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Foto atualizada!')
        return redirect('gestao:foto_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Editar Foto',
        'objeto': foto.titulo,
        'back_url': reverse('gestao:foto_lista'),
        'multipart': True,
    })


@login_required
@require_POST
def foto_deletar(request, pk):
    get_object_or_404(FotoCulto, pk=pk).delete()
    messages.success(request, 'Foto removida.')
    return redirect('gestao:foto_lista')


# ─── LOJA ────────────────────────────────────────────────────────────────────

@login_required
def produto_lista(request):
    produtos = Produto.objects.all()
    return render(request, 'gestao/produto_lista.html', {'produtos': produtos})


@login_required
def produto_criar(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Produto adicionado!')
        return redirect('gestao:produto_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Novo Produto',
        'back_url': reverse('gestao:produto_lista'),
        'multipart': True,
    })


@login_required
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Produto atualizado!')
        return redirect('gestao:produto_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Editar Produto',
        'objeto': produto.nome,
        'back_url': reverse('gestao:produto_lista'),
        'multipart': True,
    })


@login_required
@require_POST
def produto_deletar(request, pk):
    get_object_or_404(Produto, pk=pk).delete()
    messages.success(request, 'Produto removido.')
    return redirect('gestao:produto_lista')


# ─── AGENDA ──────────────────────────────────────────────────────────────────

@login_required
def evento_lista(request):
    eventos = Evento.objects.order_by('data', 'hora')
    return render(request, 'gestao/evento_lista.html', {'eventos': eventos})


@login_required
def evento_criar(request):
    form = EventoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Evento adicionado à agenda!')
        return redirect('gestao:evento_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Novo Evento',
        'back_url': reverse('gestao:evento_lista'),
    })


@login_required
def evento_editar(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    form = EventoForm(request.POST or None, instance=evento)
    if form.is_valid():
        form.save()
        messages.success(request, 'Evento atualizado!')
        return redirect('gestao:evento_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Editar Evento',
        'objeto': evento.titulo,
        'back_url': reverse('gestao:evento_lista'),
    })


@login_required
@require_POST
def evento_deletar(request, pk):
    get_object_or_404(Evento, pk=pk).delete()
    messages.success(request, 'Evento removido.')
    return redirect('gestao:evento_lista')


# ─── PARCEIROS ───────────────────────────────────────────────────────────────

@login_required
def parceiro_lista(request):
    parceiros = Empresa.objects.all()
    return render(request, 'gestao/parceiro_lista.html', {'parceiros': parceiros})


@login_required
def parceiro_criar(request):
    form = EmpresaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Empresa parceira adicionada!')
        return redirect('gestao:parceiro_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Nova Empresa Parceira',
        'back_url': reverse('gestao:parceiro_lista'),
        'multipart': True,
    })


@login_required
def parceiro_editar(request, pk):
    parceiro = get_object_or_404(Empresa, pk=pk)
    form = EmpresaForm(request.POST or None, request.FILES or None, instance=parceiro)
    if form.is_valid():
        form.save()
        messages.success(request, 'Empresa atualizada!')
        return redirect('gestao:parceiro_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Editar Empresa',
        'objeto': parceiro.nome,
        'back_url': reverse('gestao:parceiro_lista'),
        'multipart': True,
    })


@login_required
@require_POST
def parceiro_deletar(request, pk):
    get_object_or_404(Empresa, pk=pk).delete()
    messages.success(request, 'Empresa removida.')
    return redirect('gestao:parceiro_lista')


# ─── NOVOS MEMBROS ────────────────────────────────────────────────────────────

@login_required
def membro_lista(request):
    status = request.GET.get('status', 'pendente')
    if status == 'atendido':
        membros = NovoMembro.objects.filter(atendido=True)
    else:
        membros = NovoMembro.objects.filter(atendido=False)
    return render(request, 'gestao/membro_lista.html', {
        'membros': membros,
        'status': status,
        'total_pendentes': NovoMembro.objects.filter(atendido=False).count(),
    })


@login_required
@require_POST
def membro_atender(request, pk):
    membro = get_object_or_404(NovoMembro, pk=pk)
    membro.atendido = True
    membro.save()
    messages.success(request, f'"{membro.nome}" marcado como atendido.')
    return redirect('gestao:membro_lista')


@login_required
@require_POST
def membro_deletar(request, pk):
    get_object_or_404(NovoMembro, pk=pk).delete()
    messages.success(request, 'Registro removido.')
    return redirect('gestao:membro_lista')


def novo_membro_form(request):
    """Formulário público de cadastro de novos membros (sem login)."""
    form = NovoMembroForm(request.POST or None)
    enviado = False
    if request.method == 'POST' and form.is_valid():
        form.save()
        enviado = True
    return render(request, 'gestao/novo_membro_form.html', {
        'form': form,
        'enviado': enviado,
    })


# ─── CONSAGRAÇÃO / VIGÍLIA DE ORAÇÃO ──────────────────────────────────────────

@login_required
def vigilia_lista(request):
    vigilias = ConsagracaoOracao.objects.all()
    return render(request, 'gestao/vigilia_lista.html', {'vigilias': vigilias})


@login_required
def vigilia_criar(request):
    form = ConsagracaoOracaoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Consagração convocada com sucesso!')
        return redirect('gestao:vigilia_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Convocar Vigília / Consagração de Oração',
        'back_url': reverse('gestao:vigilia_lista'),
    })


@login_required
def vigilia_editar(request, pk):
    vigilia = get_object_or_404(ConsagracaoOracao, pk=pk)
    form = ConsagracaoOracaoForm(request.POST or None, instance=vigilia)
    if form.is_valid():
        form.save()
        messages.success(request, 'Consagração atualizada!')
        return redirect('gestao:vigilia_lista')
    return render(request, 'gestao/form.html', {
        'form': form,
        'titulo': 'Editar Consagração',
        'objeto': vigilia.titulo,
        'back_url': reverse('gestao:vigilia_lista'),
    })


@login_required
@require_POST
def vigilia_deletar(request, pk):
    get_object_or_404(ConsagracaoOracao, pk=pk).delete()
    messages.success(request, 'Consagração removida.')
    return redirect('gestao:vigilia_lista')


@login_required
def vigilia_horarios(request, pk):
    vigilia = get_object_or_404(ConsagracaoOracao, pk=pk)
    horarios_map = {h.hora_inicio: h for h in vigilia.horarios.all()}
    slots = []
    for slot_dt in vigilia.get_slots():
        slots.append({
            'hora': slot_dt,
            'inscricao': horarios_map.get(slot_dt),
        })
    return render(request, 'gestao/vigilia_horarios.html', {
        'vigilia': vigilia,
        'slots': slots,
    })


@login_required
@require_POST
def vigilia_remover_inscricao(request, pk):
    inscricao = get_object_or_404(HorarioOracao, pk=pk)
    vigilia_pk = inscricao.consagracao.pk
    inscricao.delete()
    messages.success(request, 'Inscrição removida.')
    return redirect('gestao:vigilia_horarios', pk=vigilia_pk)


