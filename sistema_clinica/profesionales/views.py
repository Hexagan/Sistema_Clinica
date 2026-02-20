from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Profesional, Especialidad

class ListaProfesionalesView(ListView):
    model = Profesional
    template_name = "profesionales/lista_profesionales.html"
    context_object_name = "profesionales"

    def get_queryset(self):
        return (
            Profesional.objects
            .select_related("especialidad")
            .prefetch_related("servicios")
            .all()
        )


class DetalleProfesionalView(DetailView):
    model = Profesional
    template_name = "profesionales/detalle_profesional.html"
    context_object_name = "profesional"
    pk_url_kwarg = "profesional_id"

    def get_queryset(self):
        return (
            Profesional.objects
            .select_related("especialidad")
            .prefetch_related("servicios")
        )


class ListaEspecialidadesView(ListView):
    model = Especialidad
    template_name = "profesionales/lista_especialidades.html"
    context_object_name = "especialidades"

    def get_queryset(self):
        return Especialidad.objects.all()
