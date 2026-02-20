import os
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from pacientes.models import Estudio
from pacientes.mixins import PacienteAccessMixin


class EstudiosView(LoginRequiredMixin, PacienteAccessMixin, View):
    template_name = "pacientes/estudios.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()
        est = Estudio.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha_estudio", "-creado")

        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente_id,
            "estudios": est,
        })


class CargarEstudioView(LoginRequiredMixin, PacienteAccessMixin, View):
    template_name = "pacientes/cargar_estudio.html"

    def get(self, request, paciente_id):
        return render(request, self.template_name, {
            "paciente": self.get_paciente(),
            "paciente_id": paciente_id,
        })

    def post(self, request, paciente_id):
        paciente = self.get_paciente()
        fecha = request.POST.get("fecha_estudio")
        obs = request.POST.get("observaciones", "")
        archivo = request.FILES.get("archivo")

        if not fecha:
            messages.error(request, "Debe indicar la fecha.")
            return redirect("pacientes:cargar_estudio", paciente_id=paciente_id)

        if not archivo:
            messages.error(request, "Debe subir un archivo.")
            return redirect("pacientes:cargar_estudio", paciente_id=paciente_id)

        ext = os.path.splitext(archivo.name)[1].lower()
        if ext not in [".pdf", ".jpg", ".jpeg", ".png"]:
            messages.error(request, "Formato inválido.")
            return redirect("pacientes:cargar_estudio", paciente_id=paciente_id)

        Estudio.objects.create(
            paciente=paciente,
            fecha_estudio=fecha,
            observaciones=obs,
            archivo=archivo
        )

        messages.success(request, "Estudio cargado.")
        return redirect("pacientes:estudios", paciente_id=paciente_id)
