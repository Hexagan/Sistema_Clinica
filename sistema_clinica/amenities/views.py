# amenities/views.py
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from pacientes.models import Paciente
from .models import Amenity, BeneficioOtorgado


class PacienteFromPerfilMixin(LoginRequiredMixin):

    def get_paciente(self, paciente_id):
        perfil = self.request.user.perfil
        return perfil.pacientes.get(pk=paciente_id)


# ----------------------------------------------------------
# Vista genérica para un Amenity
# ----------------------------------------------------------

class AmenityBaseView(LoginRequiredMixin, TemplateView):
    template_name = "amenities/base_amenity.html"  
    amenity_nombre = None 

    def get_context_data(self, paciente_id, **kwargs):
        context = super().get_context_data(**kwargs)

        perfil = self.request.user.perfil
        paciente = perfil.pacientes.get(pk=paciente_id)

        amenity = get_object_or_404(Amenity, nombre=self.amenity_nombre)

        beneficios = amenity.beneficios.filter(activo=True)

        beneficios_otorgados = list(
            BeneficioOtorgado.objects.filter(
                paciente=paciente,
                beneficio__amenity=amenity
            ).select_related("beneficio")
        )

        # Lista de IDs de beneficios obtenidos
        beneficios_otorgados_ids = {b.beneficio.id for b in beneficios_otorgados}

        context.update({
            "paciente": paciente,
            "amenity": amenity,
            "beneficios": beneficios,
            "beneficios_otorgados_ids": beneficios_otorgados_ids,
        })

        return context


# VISTAS ESPECÍFICAS (solo definen nombre y template)

class GimnasioView(AmenityBaseView):
    amenity_nombre = "Gimnasio"
    template_name = "amenities/gimnasio.html"


class KioscoView(AmenityBaseView):
    amenity_nombre = "Kiosco y Nutrición"
    template_name = "amenities/kiosco.html"


class NutricionView(AmenityBaseView):
    amenity_nombre = "Relajación y Mindfulness"
    template_name = "amenities/nutricion.html"


class TalleresView(AmenityBaseView):
    amenity_nombre = "Talleres y Asesoramiento de Salud"
    template_name = "amenities/talleres.html"
