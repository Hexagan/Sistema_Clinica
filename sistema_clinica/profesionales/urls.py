# profesionales/urls.py
from django.urls import path
from .views import (
    ListaProfesionalesView,
    DetalleProfesionalView,
    ListaEspecialidadesView,
)

app_name = "profesionales"

urlpatterns = [
    path("", ListaProfesionalesView.as_view(), name="lista_profesionales"),
    path("<int:profesional_id>/", DetalleProfesionalView.as_view(), name="detalle_profesional"),
    path("especialidades/", ListaEspecialidadesView.as_view(), name="lista_especialidades"),
]
