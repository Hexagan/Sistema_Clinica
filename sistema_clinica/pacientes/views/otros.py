# pacientes/views/otros.py
# (Medicamentos, mis médicos, cartilla, teleconsultas, diario)

from django.views import View
from django.utils.translation import activate
from django.shortcuts import render
from pacientes.mixins import PacienteAccessMixin
from pacientes.models import Estudio
from profesionales.models import Profesional
from django.shortcuts import redirect

class MedicamentosView(PacienteAccessMixin, View):
    template_name = "pacientes/medicamentos.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()
        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente_id,
            "recetas": paciente.recetas.filter(activa=True),
        })


class MisMedicosView(PacienteAccessMixin, View):
    template_name = "pacientes/mis_medicos.html"

    def get(self, request, paciente_id):

        paciente = self.paciente

        profesionales = Profesional.objects.filter(
            turno__paciente=paciente
        ).distinct()

        return render(request, self.template_name, {
            "paciente": paciente,
            "profesionales": profesionales,
        })


class TeleconsultasView(PacienteAccessMixin, View):
    template_name = "pacientes/teleconsultas.html"

    def get(self, request, paciente_id):
        return render(request, self.template_name, {
            "paciente": self.get_paciente(),
            "paciente_id": paciente_id,
        })


class MiDiarioView(PacienteAccessMixin, View):
    template_name = "pacientes/mi_diario.html"

    def get(self, request, paciente_id):
        activate("es")

        paciente = self.get_paciente()
        ordenar = request.GET.get("ordenar", "fecha")
        estudios = Estudio.objects.filter(paciente=paciente)

        if ordenar == "descripcion":
            estudios = estudios.order_by("observaciones")
        else:
            estudios = estudios.order_by("-fecha_estudio")

        grupos = {}
        for doc in estudios:
            mes = doc.fecha_estudio.strftime("%B %Y").capitalize()
            grupos.setdefault(mes, []).append(doc)

        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente_id,
            "ordenar": ordenar,
            "grupos": grupos,
        })

class ConsultasGestionesView(PacienteAccessMixin, View):
    template_name = "pacientes/consultas_gestiones.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()
        return render(request, self.template_name, {
            "paciente": paciente,
            "paciente_id": paciente_id,
        })

    def post(self, request, paciente_id):
        # Más adelante podrás agregar lógica interna
        return redirect("pacientes:consultas_gestiones", paciente_id=paciente_id)

class CoberturaMedicaView(PacienteAccessMixin, View):
    template_name = "pacientes/cobertura_medica.html"

    def get(self, request, paciente_id):
        return render(request, self.template_name, {
            "paciente": self.get_paciente(),
            "paciente_id": paciente_id,
        })