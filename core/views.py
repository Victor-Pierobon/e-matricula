from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InstituicaoRegistrationForm, DocenteRegistrationForm, DiscenteRegistrationForm, LoginForm
from .models import Instituicao, Docente, Discente, ComponenteCurricular, Serie, Turma, MatriculaDiscente, Aula
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, time

# Create your views here.

def index(request):
    return render(request, 'html/index.html')

def instituicao(request):
    return render(request, 'html/instituicao.html')

def docente(request):
    return render(request, 'html/docente.html')

def login_discente(request):
    return render(request, 'html/login-discente.html')

def register_instituicao(request):
    if request.method == 'POST':
        form = InstituicaoRegistrationForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            
            # Criar instituição
            instituicao = form.save(commit=False)
            instituicao.user = user
            instituicao.save()
            
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('login')
    else:
        form = InstituicaoRegistrationForm()
    return render(request, 'html/register_instituicao.html', {'form': form})

def register_docente(request):
    if request.method == 'POST':
        form = DocenteRegistrationForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Criar docente
            docente = form.save(commit=False)
            docente.user = user
            docente.save()
            
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('login')
    else:
        form = DocenteRegistrationForm()
    return render(request, 'html/register_docente.html', {'form': form})

def register_discente(request):
    if request.method == 'POST':
        form = DiscenteRegistrationForm(request.POST)
        if form.is_valid():
            # Criar usuário
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Criar discente
            discente = form.save(commit=False)
            discente.user = user
            discente.save()
            
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('login')
    else:
        form = DiscenteRegistrationForm()
    return render(request, 'html/register_discente.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Redireciona para o painel apropriado
                if hasattr(user, 'instituicao'):
                    return redirect('painel_instituicao')
                elif hasattr(user, 'docente'):
                    return redirect('painel_docente')
                elif hasattr(user, 'discente'):
                    return redirect('painel_discente')
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'html/login.html', {'form': form})

@login_required
def gerenciar_componentes(request):
    if not hasattr(request.user, 'instituicao'):
        messages.error(request, 'Acesso permitido apenas para instituições.')
        return redirect('index')
    
    componentes = ComponenteCurricular.objects.filter(instituicao=request.user.instituicao)
    return render(request, 'html/gerenciar_componentes.html', {
        'componentes': componentes,
        'areas': ComponenteCurricular.AREA_CHOICES,
        'tipos': ComponenteCurricular.TIPO_CHOICES
    })

@login_required
def adicionar_componente(request):
    if not hasattr(request.user, 'instituicao'):
        messages.error(request, 'Acesso permitido apenas para instituições.')
        return redirect('index')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        area = request.POST.get('area')
        tipo = request.POST.get('tipo')
        carga_horaria = request.POST.get('carga_horaria')
        
        componente = ComponenteCurricular.objects.create(
            nome=nome,
            area=area,
            tipo=tipo,
            carga_horaria=carga_horaria,
            instituicao=request.user.instituicao
        )
        
        messages.success(request, 'Componente curricular adicionado com sucesso!')
        return redirect('gerenciar_componentes')
    
    return render(request, 'html/adicionar_componente.html', {
        'areas': ComponenteCurricular.AREA_CHOICES,
        'tipos': ComponenteCurricular.TIPO_CHOICES
    })

@login_required
def escolher_itinerarios(request):
    if not hasattr(request.user, 'discente'):
        messages.error(request, 'Acesso permitido apenas para discentes.')
        return redirect('index')
    
    if request.method == 'POST':
        itinerarios_ids = request.POST.getlist('itinerarios')
        turma_id = request.POST.get('turma')
        
        turma = get_object_or_404(Turma, id=turma_id)
        matricula, created = MatriculaDiscente.objects.get_or_create(
            discente=request.user.discente,
            turma=turma
        )
        
        matricula.itinerarios_escolhidos.set(itinerarios_ids)
        messages.success(request, 'Itinerários escolhidos com sucesso!')
        return redirect('login_discente')
    
    turmas = Turma.objects.filter(serie__instituicao=request.user.discente.instituicao)
    itinerarios = ComponenteCurricular.objects.filter(
        instituicao=request.user.discente.instituicao,
        tipo='ITINERARIO'
    )
    
    return render(request, 'html/escolher_itinerarios.html', {
        'turmas': turmas,
        'itinerarios': itinerarios
    })

@login_required
def visualizar_matricula(request):
    if not hasattr(request.user, 'discente'):
        messages.error(request, 'Acesso permitido apenas para discentes.')
        return redirect('index')
    
    matricula = MatriculaDiscente.objects.filter(discente=request.user.discente).first()
    if not matricula:
        messages.warning(request, 'Você ainda não possui matrícula.')
        return redirect('escolher_itinerarios')
    
    return render(request, 'html/visualizar_matricula.html', {
        'matricula': matricula
    })

@login_required
def painel_instituicao(request):
    if not hasattr(request.user, 'instituicao'):
        messages.error(request, 'Acesso permitido apenas para instituições.')
        return redirect('index')
    
    instituicao = request.user.instituicao
    
    # Estatísticas gerais
    total_turmas = Turma.objects.filter(instituicao=instituicao).count()
    total_docentes = Docente.objects.filter(instituicao=instituicao).count()
    total_discentes = Discente.objects.filter(instituicao=instituicao).count()
    total_componentes = ComponenteCurricular.objects.filter(instituicao=instituicao).count()
    
    # Últimas atividades
    ultimas_atividades = [
        {
            'data': timezone.now(),
            'descricao': 'Nova turma criada',
            'status': 'Concluído',
            'status_class': 'success'
        },
        {
            'data': timezone.now(),
            'descricao': 'Componente curricular atualizado',
            'status': 'Em andamento',
            'status_class': 'warning'
        }
    ]
    
    context = {
        'total_turmas': total_turmas,
        'total_docentes': total_docentes,
        'total_discentes': total_discentes,
        'total_componentes': total_componentes,
        'ultimas_atividades': ultimas_atividades
    }
    
    return render(request, 'html/instituicao.html', context)

@login_required
def painel_docente(request):
    if not hasattr(request.user, 'docente'):
        messages.error(request, 'Acesso permitido apenas para docentes.')
        return redirect('index')
    
    docente = request.user.docente
    
    # Estatísticas gerais
    total_turmas = Turma.objects.filter(aula__docente=docente).distinct().count()
    total_alunos = MatriculaDiscente.objects.filter(turma__aula__docente=docente).distinct().count()
    total_componentes = ComponenteCurricular.objects.filter(aula__docente=docente).distinct().count()
    
    # Aulas de hoje
    hoje = timezone.now().date()
    aulas_hoje = Aula.objects.filter(
        docente=docente,
        dia_semana=hoje.isoweekday()
    ).count()
    
    aulas_hoje_list = Aula.objects.filter(
        docente=docente,
        dia_semana=hoje.isoweekday()
    ).select_related('componente', 'turma')
    
    # Próximas aulas
    proximas_aulas = Aula.objects.filter(
        docente=docente,
        dia_semana__gt=hoje.isoweekday()
    ).select_related('componente', 'turma').order_by('dia_semana', 'hora_inicio')[:5]
    
    # Turmas ativas
    turmas = Turma.objects.filter(
        aula__docente=docente
    ).distinct().annotate(
        total_alunos=Count('matriculadiscente')
    ).select_related('serie')
    
    context = {
        'total_turmas': total_turmas,
        'aulas_hoje': aulas_hoje,
        'total_alunos': total_alunos,
        'total_componentes': total_componentes,
        'aulas_hoje_list': aulas_hoje_list,
        'proximas_aulas': proximas_aulas,
        'turmas': turmas
    }
    
    return render(request, 'html/docente.html', context)

@login_required
def painel_discente(request):
    if not hasattr(request.user, 'discente'):
        messages.error(request, 'Acesso permitido apenas para discentes.')
        return redirect('index')
    
    discente = request.user.discente
    
    # Estatísticas gerais
    total_componentes = MatriculaDiscente.objects.filter(discente=discente).count()
    total_itinerarios = MatriculaDiscente.objects.filter(
        discente=discente,
        componente__tipo='ITINERARIO'
    ).count()
    
    # Carga horária total
    carga_horaria_total = MatriculaDiscente.objects.filter(
        discente=discente
    ).aggregate(
        total=Sum('componente__carga_horaria')
    )['total'] or 0
    
    # Aulas de hoje
    hoje = timezone.now().date()
    aulas_hoje = Aula.objects.filter(
        turma__matriculadiscente__discente=discente,
        data=hoje
    ).count()
    
    aulas_hoje_list = Aula.objects.filter(
        turma__matriculadiscente__discente=discente,
        data=hoje
    ).select_related('componente', 'turma')
    
    # Próximas aulas
    proximas_aulas = Aula.objects.filter(
        turma__matriculadiscente__discente=discente,
        data__gt=hoje
    ).select_related('componente', 'turma').order_by('data', 'horario_inicio')[:5]
    
    # Itinerários escolhidos
    itinerarios = ComponenteCurricular.objects.filter(
        matriculadiscente__discente=discente,
        tipo='ITINERARIO'
    ).distinct()
    
    # Grade completa
    grade = MatriculaDiscente.objects.filter(
        discente=discente
    ).select_related(
        'componente',
        'turma',
        'turma__docente'
    )
    
    context = {
        'aulas_hoje': aulas_hoje,
        'total_componentes': total_componentes,
        'total_itinerarios': total_itinerarios,
        'carga_horaria_total': carga_horaria_total,
        'aulas_hoje_list': aulas_hoje_list,
        'proximas_aulas': proximas_aulas,
        'itinerarios': itinerarios,
        'grade': grade
    }
    
    return render(request, 'html/discente-painel.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('index')

@login_required
def minhas_aulas(request):
    if not hasattr(request.user, 'docente'):
        messages.error(request, 'Acesso permitido apenas para docentes.')
        return redirect('index')
    
    docente = request.user.docente
    aulas = Aula.objects.filter(
        turma__docente=docente
    ).select_related('componente', 'turma').order_by('data', 'horario_inicio')
    
    return render(request, 'html/minhas_aulas.html', {
        'aulas': aulas
    })

@login_required
def minhas_turmas(request):
    if not hasattr(request.user, 'docente'):
        messages.error(request, 'Acesso permitido apenas para docentes.')
        return redirect('index')
    
    docente = request.user.docente
    turmas = Turma.objects.filter(
        docente=docente
    ).annotate(
        total_alunos=Count('matriculadiscente')
    ).select_related('componente')
    
    return render(request, 'html/minhas_turmas.html', {
        'turmas': turmas
    })

@login_required
def editar_componente(request, pk):
    if not hasattr(request.user, 'instituicao'):
        messages.error(request, 'Acesso permitido apenas para instituições.')
        return redirect('index')
    
    componente = get_object_or_404(ComponenteCurricular, pk=pk, instituicao=request.user.instituicao)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        area = request.POST.get('area')
        tipo = request.POST.get('tipo')
        carga_horaria = request.POST.get('carga_horaria')
        
        componente.nome = nome
        componente.area = area
        componente.tipo = tipo
        componente.carga_horaria = carga_horaria
        componente.save()
        
        messages.success(request, 'Componente curricular atualizado com sucesso!')
        return redirect('gerenciar_componentes')
    
    return render(request, 'html/editar_componente.html', {
        'componente': componente,
        'areas': ComponenteCurricular.AREA_CHOICES,
        'tipos': ComponenteCurricular.TIPO_CHOICES
    })

@login_required
def excluir_componente(request, pk):
    if not hasattr(request.user, 'instituicao'):
        messages.error(request, 'Acesso permitido apenas para instituições.')
        return redirect('index')
    
    componente = get_object_or_404(ComponenteCurricular, pk=pk, instituicao=request.user.instituicao)
    
    if request.method == 'POST':
        componente.delete()
        messages.success(request, 'Componente curricular excluído com sucesso!')
        return redirect('gerenciar_componentes')
    
    return render(request, 'html/excluir_componente.html', {
        'componente': componente
    })
