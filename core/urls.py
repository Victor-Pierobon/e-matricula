from django.urls import path
from . import views

urlpatterns = [
    # URLs públicas
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/instituicao/', views.register_instituicao, name='register_instituicao'),
    path('register/docente/', views.register_docente, name='register_docente'),
    path('register/discente/', views.register_discente, name='register_discente'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs da Instituição
    path('painel/instituicao/', views.painel_instituicao, name='painel_instituicao'),
    path('componentes/', views.gerenciar_componentes, name='gerenciar_componentes'),
    path('componentes/adicionar/', views.adicionar_componente, name='adicionar_componente'),
    path('componentes/editar/<int:pk>/', views.editar_componente, name='editar_componente'),
    path('componentes/excluir/<int:pk>/', views.excluir_componente, name='excluir_componente'),
    
    # URLs do Docente
    path('painel/docente/', views.painel_docente, name='painel_docente'),
    path('docente/aulas/', views.minhas_aulas, name='minhas_aulas'),
    path('docente/turmas/', views.minhas_turmas, name='minhas_turmas'),
    
    # URLs do Discente
    path('painel/discente/', views.painel_discente, name='painel_discente'),
    path('matricula/', views.visualizar_matricula, name='visualizar_matricula'),
    path('matricula/escolher-itinerarios/', views.escolher_itinerarios, name='escolher_itinerarios'),
] 