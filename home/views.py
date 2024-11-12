from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def login_discente(request):
    return render(request, 'home/login_discente.html')

def discente_painel_opcoes(request):
    return render(request, 'home/discente_painel_opcoes.html')
