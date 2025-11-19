from django.urls import path
from . import views

app_name = "turnos"

urlpatterns = [
    path("solicitar/<int:paciente_id>/", views.solicitar_turno, name="solicitar_turno"),
    path("historial/", views.historial_turnos, name="historial_turnos"),
    path("<int:turno_id>/", views.ver_turno, name="ver_turno"),
    path("agendados/", views.turnos_agendados, name="turnos_agendados"),
    path("ver_turnos/<int:paciente_id>/", views.ver_turno, name="ver_turnos"),
]
