# usuarios/views.py (VERSION COMPLETA CON CLASES)

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from .forms import RegistroCustomForm, LoginForm
from .models import PerfilUsuario
from pacientes.models import Paciente


# =====================================================
# 🔐 LOGIN (Class-Based)
# =====================================================
class UsuarioLoginView(FormView):
    template_name = "usuarios/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("usuarios:perfil")

    def form_valid(self, form):
        usuario = form.get_user()
        login(self.request, usuario)
        return super().form_valid(form)


# =====================================================
# 📝 REGISTRO DE USUARIO (Class-Based)
# =====================================================
class RegistrarUsuarioView(FormView):
    template_name = "usuarios/registrar_custom.html"
    form_class = RegistroCustomForm
    success_url = reverse_lazy("usuarios:perfil")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        usuario = User.objects.create_user(
            username=username,
            password=password
        )

        PerfilUsuario.objects.create(usuario=usuario)

        login(self.request, usuario)
        return super().form_valid(form)


# =====================================================
# 🧍 PERFIL DEL USUARIO (Class-Based)
# =====================================================
class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/perfil.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        perfil = self.request.user.perfil
        ctx["usuario"] = self.request.user
        ctx["perfil"] = perfil
        ctx["pacientes"] = perfil.pacientes.all()
        return ctx


# =====================================================
# 🔎 DETALLE DE PACIENTE DESDE USUARIO (Class-Based)
# =====================================================
class PacienteDetalleUsuarioView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = "pacientes/paciente_detalle.html"
    context_object_name = "paciente"

    def get_object(self):
        paciente = super().get_object()

        if paciente not in self.request.user.perfil.pacientes.all():
            raise PermissionError("No tenés acceso a este paciente")

        return paciente
