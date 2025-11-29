# pacientes/views/dashboard.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from pacientes.models import Paciente
from profesionales.models import Especialidad, Profesional
from pacientes.mixins import PacienteAccessMixin


class PortalPacienteView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "pacientes/portal_paciente.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        request.session["paciente_id"] = paciente.id

        return render(request, self.template_name, {
            "usuario": request.user,
            "pacientes": request.user.perfil.pacientes.all(),
            "paciente_seleccionado": paciente,
            "paciente": paciente,
            "especialidades": Especialidad.objects.all(),
            "profesionales": Profesional.objects.all(),
            "paciente_id": paciente.id,
        })


class CrearPacienteView(LoginRequiredMixin, View):
    template_name = "pacientes/crear_paciente.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')

        if Paciente.objects.filter(dni=dni).exists():
            return render(request, self.template_name, {"error": "Ya existe un paciente con ese DNI."})

        nuevo = Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento'),
            obra_social=request.POST.get('obra_social'),
            perfil_usuario=request.user.perfil
        )

        request.user.perfil.pacientes.add(nuevo)
        return redirect("pacientes:creacion_paciente_exitosa")


class CreacionPacienteExitosaView(LoginRequiredMixin, TemplateView):
    template_name = "pacientes/creacion_paciente_exitosa.html"


class PacienteDetalleView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = "pacientes/paciente_detalle.html"
    context_object_name = "paciente"


class ListaPacientesView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/lista_pacientes.html"
    context_object_name = "pacientes"
    ordering = ["apellido", "nombre"]
