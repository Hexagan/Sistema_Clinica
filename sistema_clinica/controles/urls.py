from django.urls import path
from . import views

app_name = "controles"

urlpatterns = [
    path("peso-altura/<int:paciente_id>/", views.PesoAlturaView.as_view(), name="peso_altura"),
    path("temperatura/<int:paciente_id>/", views.TemperaturaView.as_view(), name="temperatura"),
    path("frecuencia-cardiaca/<int:paciente_id>/", views.FrecuenciaCardiacaView.as_view(), name="frecuencia_cardiaca"),
    path("presion/<int:paciente_id>/", views.PresionArterialView.as_view(), name="presion_arterial"),
    path("glucemia/<int:paciente_id>/", views.GlucemiaView.as_view(), name="glucemia"),
    path("frecuencia-respiratoria/<int:paciente_id>/", views.FrecuenciaRespiratoriaView.as_view(), name="frecuencia_respiratoria"),
    path("disnea/<int:paciente_id>/", views.DisneaView.as_view(), name="disnea"),
    path("saturacion/<int:paciente_id>/", views.SaturacionOxigenoView.as_view(), name="saturacion_oxigeno"),
    path("indicaciones/<int:paciente_id>/", views.IndicacionesView.as_view(), name="indicaciones"),
]
