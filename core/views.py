from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import InstituicaoRegistrationForm, DocenteRegistrationForm, DiscenteRegistrationForm, LoginForm
from .models import Instituicao, Docente, Discente

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
                # Redirecionar com base no tipo de usuário
                if hasattr(user, 'instituicao'):
                    return redirect('instituicao')
                elif hasattr(user, 'docente'):
                    return redirect('docente')
                elif hasattr(user, 'discente'):
                    return redirect('login_discente')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'html/login.html', {'form': form})
