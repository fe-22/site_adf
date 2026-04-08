from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import IntegrityError
from .models import Produto, Evento, FotoCulto, Empresa
from gestao.models import Reuniao, ConsagracaoOracao, HorarioOracao
from gestao.forms import InscricaoOracaoForm


def home(request):
    eventos_proximos = Evento.objects.filter(data__gte=timezone.now().date()).order_by('data', 'hora')[:5]
    fotos_destaque = FotoCulto.objects.filter(destaque=True)[:6]
    return render(request, 'core/home.html', {
        'eventos_proximos': eventos_proximos,
        'fotos_destaque': fotos_destaque,
    })


def loja(request):
    categoria = request.GET.get('categoria', '')
    produtos = Produto.objects.filter(disponivel=True)
    if categoria:
        produtos = produtos.filter(categoria=categoria)
    categorias = Produto.CATEGORIAS
    return render(request, 'core/loja.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_selecionada': categoria,
    })


def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk, disponivel=True)
    return render(request, 'core/produto_detalhe.html', {'produto': produto})


def agenda(request):
    eventos = Evento.objects.filter(data__gte=timezone.now().date()).order_by('data', 'hora')
    return render(request, 'core/agenda.html', {'eventos': eventos})


def galeria(request):
    fotos = FotoCulto.objects.all()
    return render(request, 'core/galeria.html', {'fotos': fotos})


def parceiros(request):
    empresas = Empresa.objects.filter(ativo=True)
    return render(request, 'core/parceiros.html', {'empresas': empresas})


def reunioes(request):
    from django.utils import timezone
    hoje = timezone.now().date()
    proximas = Reuniao.objects.filter(data__gte=hoje).order_by('data', 'hora')
    anteriores = Reuniao.objects.filter(data__lt=hoje).order_by('-data', '-hora')[:10]
    return render(request, 'core/reunioes.html', {
        'proximas': proximas,
        'anteriores': anteriores,
    })


def oracao(request):
    import datetime
    now = timezone.now()
    vigilia_ativa = ConsagracaoOracao.objects.filter(ativa=True, data_fim__gte=now).order_by('data_inicio').first()

    # POST — processar inscrição e redirecionar (PRG)
    if request.method == 'POST' and vigilia_ativa:
        form = InscricaoOracaoForm(request.POST)
        if form.is_valid():
            hora_str = form.cleaned_data['hora_inicio']
            try:
                hora_dt = datetime.datetime.fromisoformat(hora_str)
                if timezone.is_naive(hora_dt):
                    hora_dt = timezone.make_aware(hora_dt)
                valid_slots = vigilia_ativa.get_slots()
                if hora_dt not in valid_slots:
                    erro = 'Horário inválido. Por favor, tente novamente.'
                else:
                    _, created = HorarioOracao.objects.get_or_create(
                        consagracao=vigilia_ativa,
                        hora_inicio=hora_dt,
                        defaults={
                            'nome': form.cleaned_data['nome'],
                            'telefone': form.cleaned_data.get('telefone', ''),
                        }
                    )
                    if created:
                        return redirect(f"{request.path}?ok=1")
                    else:
                        erro = 'Este horário já foi assumido. Escolha outro.'
            except (ValueError, TypeError):
                erro = 'Horário inválido.'
        else:
            erro = 'Por favor, preencha todos os campos obrigatórios.'

        # Se chegou aqui, houve erro — montar slots e renderizar com erro
        slots = _build_slots(vigilia_ativa, now)
        return render(request, 'core/oracao.html', {
            'vigilia': vigilia_ativa,
            'slots': slots,
            'form': form,
            'confirmado': False,
            'erro': erro,
        })

    # GET — montar slots frescos do banco
    slots = _build_slots(vigilia_ativa, now) if vigilia_ativa else []
    confirmado = request.GET.get('ok') == '1'

    return render(request, 'core/oracao.html', {
        'vigilia': vigilia_ativa,
        'slots': slots,
        'form': InscricaoOracaoForm(),
        'confirmado': confirmado,
        'erro': None,
    })


def _build_slots(vigilia, now):
    horarios_map = {h.hora_inicio: h for h in vigilia.horarios.all()}
    slots = []
    for slot_dt in vigilia.get_slots():
        slots.append({
            'hora': slot_dt,
            'inscricao': horarios_map.get(slot_dt),
            'passado': slot_dt < now,
        })
    return slots
