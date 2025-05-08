from django.shortcuts import render, get_object_or_404, redirect
from .models import GradeCurricular, Materia, Matricula
from django.contrib.auth.decorators import login_required
from .forms import MatriculaForm
from django.contrib import messages

# Create your views here.
def home(request):
    """View para a oágina inicial"""
    grades = GradeCurricular.objects.all()
    return render(request, 'home.html', {'grades': grades})

def grade_curricular_detalhe(request, grade_id):
    """
    View para exibir os detalhes de uma grade curricular específica (incluindo as matérias).
    """
    grade = get_object_or_404(GradeCurricular, pk=grade_id)
    # Obtém a grade ou retorna 404 se não existir
    return render(request, 'grade_curricular_detalhe.html', {'grade': grade})

def materia_busca(request):
    """
    View para a busca de matérias.  Lida com a requisição GET (para exibir o formulário de busca)
    e POST (para processar a busca).
    """
    termo_busca = request.GET.get('q')  # Obtém o termo de busca da URL (?q=...)
    resultados = []

    if termo_busca:  # Se um termo de busca foi fornecido
        resultados = Materia.objects.filter(
            Q(nome__icontains=termo_busca) |  # Busca no nome da matéria (case-insensitive)
            Q(codigo__icontains=termo_busca) |  # Busca no código da matéria
            Q(professor__first_name__icontains=termo_busca) | # Busca no nome
            Q(professor__last_name__icontains=termo_busca)   # Busca no sobrenome
        ).distinct()  # Evita resultados duplicados
    return render(request, 'materia_busca.htlm', {
        'termo_busca': termo_busca,
        'resultados': resultados
    })

@login_required  # Exige que o usuário esteja logado para acessar esta view
def matricula_criar(request):
    """
    View para criar uma nova matrícula.
    """
    if request.method == 'POST':
        form = MatriculaForm(request.POST, user=request.user)
        if form.is_valid():
            matricula = form.save()
            messages.success(request, 'Matrícula criada com sucesso! Aguarde a aprovação.') #Adiciona uma mensagem de sucesso
            return redirect('matricula_detalhe', matricula_id=matricula.id)  # Redireciona para a view de detalhes da matrícula
    else:
        form = MatriculaForm(user=request.user)  # Passa o usuário para o formulário

    return render(request, 'matricula_criar.html', {'form': form})


@login_required
def matricula_detalhe(request, matricula_id):
    """
    View para exibir os detalhes de uma matrícula específica.
    """
    matricula = get_object_or_404(Matricula, pk=matricula_id)

    # Verifica se o usuário tem permissão para ver esta matrícula (se é o dono ou um administrador)
    if request.user != matricula.aluno and not request.user.is_staff:
        return redirect('home')   #Redireciona caso o usuario não for o aluno e nem administrador
    return render(request, 'matricula_detalhe.html', {'matricula': matricula})


@login_required
def matriculas_listar(request):
    """
    View para listar as matrículas do aluno logado.
    """
    matriculas = Matricula.objects.filter(aluno=request.user).order_by('-data_criacao')
    # Filtra as matrículas pelo aluno logado
    return render(request, 'matriculas_listar.html', {'matriculas': matriculas})

# --- Views para Administradores/Servidores ---

@login_required
def matriculas_pendentes(request):
    """
    View para listar as matrículas pendentes de aprovação (para servidores).
    """
    if not request.user.is_staff:  # Verifica se o usuário é um servidor (staff)
        return redirect('home') #Redireciona o usuário para a home caso ele não seja um administrador

    matriculas = Matricula.objects.filter(status='pendente').order_by('data_criacao')
    return render(request, 'matriculas_pendentes.html', {'matriculas': matriculas})

@login_required
def matricula_aprovar(request, matricula_id):
    """
    View para aprovar uma matrícula (para servidores).
    """
    if not request.user.is_staff:
        return redirect('home')

    matricula = get_object_or_404(Matricula, pk=matricula_id)
    if matricula.status == 'pendente':
         matricula.status = 'aprovada'
         matricula.save()
         messages.success(request, "Matrícula Aprovada com sucesso!")
    
    return redirect('matriculas_pendentes')  # Redireciona de volta para a lista de pendentes


@login_required
def matricula_rejeitar(request, matricula_id):
    """
    View para rejeitar uma matrícula (para servidores).
    """
    if not request.user.is_staff:
        return redirect('home')

    matricula = get_object_or_404(Matricula, pk=matricula_id)
    if matricula.status == 'pendente':
        matricula.status = 'rejeitada'
        matricula.save()
        messages.success(request, "Matrícula Rejeitada com sucesso!") #Adiciona mensagem de sucesso
    return redirect('matriculas_pendentes')