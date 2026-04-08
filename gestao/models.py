from django.db import models


class Reuniao(models.Model):
    TIPO_CHOICES = [
        ('geral', 'Reunião Geral'),
        ('obreiros', 'Reunião de Obreiros'),
    ]
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    data = models.DateField(verbose_name='Data')
    hora = models.TimeField(verbose_name='Hora')
    local = models.CharField(max_length=200, default='Sede Central', verbose_name='Local')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='geral', verbose_name='Tipo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'
        ordering = ['-data', '-hora']

    def __str__(self):
        return f'{self.titulo} — {self.data}'


class Presenca(models.Model):
    reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='presencas', verbose_name='Reunião')
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone (opcional)')
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
        ordering = ['nome']
        unique_together = ['reuniao', 'nome']

    def __str__(self):
        return f'{self.nome} — {self.reuniao.titulo}'


class ConsagracaoOracao(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título da Convocação')
    descricao = models.TextField(blank=True, verbose_name='Mensagem de Convocação')
    data_inicio = models.DateTimeField(verbose_name='Início da Consagração')
    data_fim = models.DateTimeField(verbose_name='Fim da Consagração')
    ativa = models.BooleanField(default=True, verbose_name='Ativa / Visível no Site')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consagração de Oração'
        verbose_name_plural = 'Consagrações de Oração'
        ordering = ['-data_inicio']

    def __str__(self):
        return self.titulo

    def get_slots(self):
        """Retorna lista de datetimes de cada slot de 1h entre início e fim."""
        from datetime import timedelta
        slots = []
        current = self.data_inicio
        while current < self.data_fim:
            slots.append(current)
            current += timedelta(hours=1)
        return slots

    def total_slots(self):
        return len(self.get_slots())

    def slots_ocupados(self):
        return self.horarios.count()


class HorarioOracao(models.Model):
    consagracao = models.ForeignKey(
        ConsagracaoOracao, on_delete=models.CASCADE,
        related_name='horarios', verbose_name='Consagração'
    )
    nome = models.CharField(max_length=200, verbose_name='Nome do Obreiro')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone (opcional)')
    hora_inicio = models.DateTimeField(verbose_name='Hora de Início')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Horário de Oração'
        verbose_name_plural = 'Horários de Oração'
        ordering = ['hora_inicio']
        unique_together = ['consagracao', 'hora_inicio']

    def __str__(self):
        return f'{self.nome} — {self.hora_inicio.strftime("%d/%m %H:%M")}'

    @property
    def hora_fim(self):
        from datetime import timedelta
        return self.hora_inicio + timedelta(hours=1)


class NovoMembro(models.Model):
    COMO_CONHECEU_CHOICES = [
        ('convite', 'Convite de amigo ou familiar'),
        ('redes_sociais', 'Redes Sociais'),
        ('youtube', 'YouTube'),
        ('passando', 'Passando pela rua'),
        ('outro', 'Outro'),
    ]
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, verbose_name='Telefone / WhatsApp')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    endereco = models.CharField(max_length=300, blank=True, verbose_name='Endereço')
    como_conheceu = models.CharField(max_length=30, choices=COMO_CONHECEU_CHOICES, verbose_name='Como nos conheceu?')
    observacoes = models.TextField(blank=True, verbose_name='Observações / Pedido de Oração')
    criado_em = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False, verbose_name='Atendido')

    class Meta:
        verbose_name = 'Novo Membro'
        verbose_name_plural = 'Novos Membros'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome
