from django.db import models


class Produto(models.Model):
    CATEGORIAS = [
        ('livro', 'Livro'),
        ('cd', 'CD / DVD'),
        ('roupa', 'Vestuário'),
        ('acessorio', 'Acessório'),
        ('outro', 'Outro'),
    ]
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='outro')
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Evento(models.Model):
    TIPOS = [
        ('culto', 'Culto'),
        ('conferencia', 'Conferência'),
        ('jovens', 'Culto de Jovens'),
        ('celula', 'Célula'),
        ('especial', 'Evento Especial'),
        ('outro', 'Outro'),
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='culto')
    data = models.DateField()
    hora = models.TimeField()
    local = models.CharField(max_length=200, default='Sede Central')
    recorrente = models.BooleanField(default=False, help_text='Evento que se repete semanalmente')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data', 'hora']

    def __str__(self):
        return f'{self.titulo} - {self.data}'


class FotoCulto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.CharField(max_length=300, blank=True)
    imagem = models.ImageField(upload_to='fotos/')
    data_culto = models.DateField()
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto de Culto'
        verbose_name_plural = 'Fotos de Cultos'
        ordering = ['-data_culto']

    def __str__(self):
        return f'{self.titulo} - {self.data_culto}'


class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to='empresas/', blank=True, null=True)
    site = models.URLField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa Parceira'
        verbose_name_plural = 'Empresas Parceiras'
        ordering = ['nome']

    def __str__(self):
        return self.nome
