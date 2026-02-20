from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from profesionales.models import Especialidad, Profesional
from pacientes.mixins import PacienteAccessMixin

class PortalPacienteView(LoginRequiredMixin, PacienteAccessMixin, TemplateView):
    template_name = "pacientes/portal_paciente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        perfil = self.request.user.perfil

        context.update({
            "usuario": self.request.user,
            "pacientes": perfil.pacientes.all(),
            "paciente": self.paciente,
            "paciente_seleccionado": self.paciente,
            "paciente_id": self.paciente.id,
            "especialidades": Especialidad.objects.all(),
            "profesionales": Profesional.objects.all(),
        })

        return context
