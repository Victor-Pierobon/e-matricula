from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Instituicao(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

class Discente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

class Serie(models.Model):
    ANO_CHOICES = [
        ('1', '1ª Série'),
        ('2', '2ª Série'),
        ('3', '3ª Série'),
    ]
    
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    ano = models.CharField(max_length=1, choices=ANO_CHOICES)
    ano_letivo = models.IntegerField()
    
    class Meta:
        unique_together = ['instituicao', 'ano', 'ano_letivo']
    
    def __str__(self):
        return f"{self.get_ano_display()} - {self.ano_letivo}"

class Turma(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    turno = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nome} - {self.serie}"

class ComponenteCurricular(models.Model):
    AREA_CHOICES = [
        ('LINGUAGENS', 'Linguagens e suas Tecnologias'),
        ('MATEMATICA', 'Matemática e suas Tecnologias'),
        ('NATUREZA', 'Ciências da Natureza e suas Tecnologias'),
        ('HUMANAS', 'Ciências Humanas e Sociais Aplicadas'),
        ('TECNICO', 'Formação Técnica e Profissional'),
    ]
    
    TIPO_CHOICES = [
        ('BNCC', 'Base Nacional Comum Curricular'),
        ('ITINERARIO', 'Itinerário Formativo'),
    ]
    
    nome = models.CharField(max_length=100)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    carga_horaria = models.IntegerField(help_text="Carga horária em horas")
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class MatriculaDiscente(models.Model):
    discente = models.ForeignKey(Discente, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)
    itinerarios_escolhidos = models.ManyToManyField(
        ComponenteCurricular,
        limit_choices_to={'tipo': 'ITINERARIO'},
        related_name='matriculas'
    )
    
    class Meta:
        unique_together = ['discente', 'turma']
    
    def __str__(self):
        return f"{self.discente} - {self.turma}"

class Aula(models.Model):
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[(i, i) for i in range(1, 8)])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    
    class Meta:
        unique_together = ['componente', 'turma', 'dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.componente} - {self.turma} - {self.get_dia_semana_display()}"
