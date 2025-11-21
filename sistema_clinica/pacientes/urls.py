from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.portal_paciente, name="portal_paciente"),
    path("paciente/<int:pk>/", views.paciente_detalle, name="paciente_detalle"),
    path("crear_paciente/", views.crear_paciente, name="crear_paciente"),
    path("creacion_paciente_exitosa/", views.creacion_paciente_exitosa, name="creacion_paciente_exitosa"),
    path("lista_pacientes/", views.lista_pacientes, name="lista_pacientes"),
    path("<int:paciente_id>/indicaciones/", views.indicaciones, name="indicaciones"),
    path("<int:paciente_id>/peso-altura/", views.peso_altura, name="peso_altura"),
    path("<int:paciente_id>/temperatura/", views.temperatura, name="temperatura"),
    path("<int:paciente_id>/frecuencia-cardiaca/", views.frecuencia_cardiaca, name="frecuencia_cardiaca"),
    path("<int:paciente_id>/presion-arterial/", views.presion_arterial, name="presion_arterial"),
    path("<int:paciente_id>/glucemia/", views.glucemia, name="glucemia"),
    path("<int:paciente_id>/frecuencia-respiratoria/", views.frecuencia_respiratoria, name="frecuencia_respiratoria"),
    path("<int:paciente_id>/saturacion-oxigeno/", views.saturacion_oxigeno, name="saturacion_oxigeno"),
    path("<int:paciente_id>/disnea/", views.disnea, name="disnea"),
]

