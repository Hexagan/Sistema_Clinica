from django.urls import path
from . import views

app_name = "controles"

urlpatterns = [
    path("saturacion/<int:paciente_id>/", views.saturacion_oxigeno, name="saturacion_oxigeno"),
    path("peso-altura/<int:paciente_id>/", views.peso_altura, name="peso_altura"),
    path("temperatura/<int:paciente_id>/", views.temperatura, name="temperatura"),
    path("frecuencia-cardiaca/<int:paciente_id>/", views.frecuencia_cardiaca, name="frecuencia_cardiaca"),
    path("presion/<int:paciente_id>/", views.presion_arterial, name="presion_arterial"),
    path("glucemia/<int:paciente_id>/", views.glucemia, name="glucemia"),
    path("frecuencia-respiratoria/<int:paciente_id>/", views.frecuencia_respiratoria, name="frecuencia_respiratoria"),
    path("disnea/<int:paciente_id>/", views.disnea, name="disnea"),
    path('indicaciones/<int:paciente_id>/', views.indicaciones, name='indicaciones'),
]
