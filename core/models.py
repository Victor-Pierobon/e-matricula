from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GradeCurricular(models.Model):
    nome = models.CharField(max_length=255)
    ano = models.IntegerField()


    def __self__(self):
        return self.nome
    
class Materia(models.Model):
    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10, unique=True)  # Código único para a matéria
    descricao = models.TextField(blank=True, null=True)  # Permite descrição vazia
    carga_horaria = models.IntegerField()
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='materias_lecionadas')
    # related_name facilita o acesso às matérias de um professor (professor.materias_lecionadas)
    grade = models.ForeignKey(GradeCurricular, on_delete=models.CASCADE, related_name='materias')
    # Uma matéria pertence a uma grade curricular
    # Outros campos, como pré-requisitos (pode ser um ManyToManyField para outras Matérias)

    def __str__(self):
        return self.nome


class Matricula(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matriculas')
    # Um aluno pode ter várias matrículas
    grade = models.ForeignKey(GradeCurricular, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia)  # Um aluno escolhe várias matérias
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação da matrícula
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ], default='pendente') #Status da matricula
    # Outros campos: justificativa de rejeição (se aplicável)

    def __str__(self):
        return f"Matrícula de {self.aluno.username} em {self.grade.nome}"

    class Meta:
        #Configura o nome que será exibido no painel adm
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"