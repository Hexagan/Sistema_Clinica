# pacientes/views/controles.py
from django.views.generic import TemplateView
from pacientes.mixins import PacienteAccessMixin


class ControlBaseView(PacienteAccessMixin, TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["paciente"] = self.get_paciente()
        ctx["paciente_id"] = self.kwargs["paciente_id"]
        return ctx


class IndicacionesView(ControlBaseView):
    template_name = "pacientes/indicaciones.html"


class PesoAlturaView(ControlBaseView):
    template_name = "pacientes/peso_altura.html"


class TemperaturaView(ControlBaseView):
    template_name = "pacientes/temperatura.html"


class FrecuenciaCardiacaView(ControlBaseView):
    template_name = "pacientes/frecuencia_cardiaca.html"


class PresionArterialView(ControlBaseView):
    template_name = "pacientes/presion_arterial.html"


class GlucemiaView(ControlBaseView):
    template_name = "pacientes/glucemia.html"


class FrecuenciaRespiratoriaView(ControlBaseView):
    template_name = "pacientes/frecuencia_respiratoria.html"


class SaturacionOxigenoView(ControlBaseView):
    template_name = "pacientes/saturacion_oxigeno.html"


class DisneaView(ControlBaseView):
    template_name = "pacientes/disnea.html"
