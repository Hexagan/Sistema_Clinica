from django.urls import path
from . import views

app_name = "turnos"

urlpatterns = [
    path("solicitar/", views.solicitar_turno, name="solicitar_turno"),
    path("exitoso/<int:turno_id>/", views.turno_exitoso, name="turno_exitoso"),
    path("historial/", views.historial_turnos, name="historial_turnos"),
    path("ver/<int:turno_id>/", views.ver_turno, name="ver_turno"),
]
