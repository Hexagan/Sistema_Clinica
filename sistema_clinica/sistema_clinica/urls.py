"""
URL configuration for sistema_clinica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("usuarios:perfil")
    return redirect("usuarios:login")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pacientes/', include('pacientes.urls')),
    path('profesionales/', include('profesionales.urls')),
    path('turnos/', include('turnos.urls', namespace="turnos")),
    path('amenities/', include('amenities.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),

    path('', home_redirect),
]

