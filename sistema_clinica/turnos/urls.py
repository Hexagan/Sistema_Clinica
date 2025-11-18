from django.urls import path
from . import views

app_name = "turnos"

urlpatterns = [
    path('solicitar_turno/<int:paciente_id>/', views.solicitar_turno, name='solicitar_turno'),
    path('turno_exitoso/', views.turno_exitoso, name='turno_exitoso'),
    path("ver_turnos/<int:paciente_id>/", views.lista_turnos, name="ver_turnos"),
]
