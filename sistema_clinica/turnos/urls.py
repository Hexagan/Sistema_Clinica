from django.urls import path
from . import views

app_name = "turnos"

urlpatterns = [
    path("solicitar/<int:paciente_id>", views.solicitar_turno, name="solicitar_turno"),
    path("exitoso/<int:paciente_id>/<int:turno_id>/", views.turno_exitoso, name="turno_exitoso"),
    path("historial/<int:paciente_id>/", views.turnos_historial, name="turnos_historial"),
    path("<int:paciente_id>/ver/<int:turno_id>/", views.ver_turno, name="ver_turno"),
    path("<int:paciente_id>/turno/<int:turno_id>/", views.ver_turno, name="ver_turno"),
    path('disponibles/', views.turnos_disponibles, name='turnos_disponibles'),
    path('reservar/', views.reservar_turno, name='reservar_turno'),
    path("agendados/<int:paciente_id>", views.turnos_agendados, name="turnos_agendados"),
    path("<int:paciente_id>/cancelar/<int:turno_id>/", views.cancelar_turno, name="cancelar_turno"),
    path("checkin/", views.checkin_qr, name="checkin_qr"),

]
