"""
URL configuration for ematricula project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import index, instituicao, docente, login_discente, register_instituicao, register_docente, register_discente, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('instituicao/', instituicao, name='instituicao'),
    path('docente/', docente, name='docente'),
    path('login-discente/', login_discente, name='login_discente'),
    path('register/instituicao/', register_instituicao, name='register_instituicao'),
    path('register/docente/', register_docente, name='register_docente'),
    path('register/discente/', register_discente, name='register_discente'),
    path('login/', login_view, name='login'),
]
