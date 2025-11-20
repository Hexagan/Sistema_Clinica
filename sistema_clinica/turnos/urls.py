from django.urls import path
from . import views

app_name = "turnos"

urlpatterns = [
    path("<int:paciente_id>/solicitar/", views.solicitar_turno, name="solicitar_turno"),
    path("<int:paciente_id>/exitoso/<int:turno_id>/", views.turno_exitoso, name="turno_exitoso"),
    path("<int:paciente_id>/historial/", views.turnos_historial, name="turnos_historial"),
    path("<int:paciente_id>/ver/<int:turno_id>/", views.ver_turno, name="ver_turno"),
    path('disponibles/', views.turnos_disponibles, name='turnos_disponibles'),
    path('reservar/', views.reservar_turno, name='reservar_turno'),
    path("<int:paciente_id>/agendados/", views.turnos_agendados, name="turnos_agendados"),
]
