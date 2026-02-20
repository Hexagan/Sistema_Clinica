from django.shortcuts import get_object_or_404
from pacientes.models import Paciente

class PacienteAccessMixin:
    """Mixin para obtener el paciente y verificar acceso."""

    def get_paciente(self):
        paciente_id = self.kwargs.get("paciente_id")

        paciente = get_object_or_404(Paciente, id=paciente_id)

        # Verificar que pertenece al usuario autenticado
        if paciente not in self.request.user.perfil.pacientes.all():
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("No tiene acceso a este paciente.")

        return paciente
