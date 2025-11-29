from django.urls import path
from . import views

app_name = "turnos"

urlpatterns = [
    path("solicitar/<int:paciente_id>/", views.SolicitarTurnoView.as_view(), name="solicitar_turno"),
    path("disponibles/", views.TurnosDisponiblesView.as_view(), name="turnos_disponibles"),
    path("reservar/", views.ReservarTurnoView.as_view(), name="reservar_turno"),
    path("exitoso/<int:paciente_id>/<int:turno_id>/", views.TurnoExitosoView.as_view(), name="turno_exitoso"),
    path("historial/<int:paciente_id>/", views.TurnosHistorialView.as_view(), name="turnos_historial"),
    path("agendados/<int:paciente_id>/", views.TurnosAgendadosView.as_view(), name="turnos_agendados"),
    path("<int:paciente_id>/ver/<int:turno_id>/", views.VerTurnoView.as_view(), name="ver_turno"),
    path("<int:paciente_id>/turno/<int:turno_id>/", views.VerTurnoView.as_view(), name="ver_turno_alt"),
    path("<int:paciente_id>/cancelar/<int:turno_id>/", views.CancelarTurnoView.as_view(), name="cancelar_turno"),
    path("checkin/", views.CheckinQRView.as_view(), name="checkin_qr"),
]
