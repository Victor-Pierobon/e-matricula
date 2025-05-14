from django.contrib import admin
from .models import Instituicao, Docente, Discente

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'endereco')
    search_fields = ('nome', 'email')

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'instituicao', 'matricula')
    search_fields = ('user__username', 'matricula')
    list_filter = ('instituicao',)

@admin.register(Discente)
class DiscenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'instituicao', 'matricula')
    search_fields = ('user__username', 'matricula')
    list_filter = ('instituicao',)
