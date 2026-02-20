from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from pacientes.models import Paciente

class PacienteAccessMixin():
    """Valida que el paciente exista y pertenezca al usuario."""
    
    paciente = None

    def dispatch(self, request, *args, **kwargs):
        paciente_id = kwargs.get("paciente_id")
        paciente = get_object_or_404(Paciente, pk=paciente_id)

        if paciente not in request.user.perfil.pacientes.all():
            return self.handle_no_permission()

        # Guardar paciente en el mixin
        self.paciente = paciente
        request.session["paciente_id"] = paciente_id

        return super().dispatch(request, *args, **kwargs)

    def get_paciente(self):
        """Devuelve el paciente cargado en dispatch."""
        return self.paciente
