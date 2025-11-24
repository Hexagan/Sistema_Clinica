from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.portal_paciente, name="portal_paciente"),
    path("paciente/<int:pk>/", views.paciente_detalle, name="paciente_detalle"),
    path("crear_paciente/", views.crear_paciente, name="crear_paciente"),
    path("creacion_paciente_exitosa/", views.creacion_paciente_exitosa, name="creacion_paciente_exitosa"),
    path("lista_pacientes/", views.lista_pacientes, name="lista_pacientes"),
   
    #Controles

    path("indicaciones/<int:paciente_id>", views.indicaciones, name="indicaciones"),
    path("peso-altura/<int:paciente_id>", views.peso_altura, name="peso_altura"),
    path("temperatura/<int:paciente_id>", views.temperatura, name="temperatura"),
    path("frecuencia-cardiaca/<int:paciente_id>/", views.frecuencia_cardiaca, name="frecuencia_cardiaca"),
    path("presion-arterial/<int:paciente_id>/", views.presion_arterial, name="presion_arterial"),
    path("glucemia/<int:paciente_id>/", views.glucemia, name="glucemia"),
    path("frecuencia-respiratoria/<int:paciente_id>/", views.frecuencia_respiratoria, name="frecuencia_respiratoria"),
    path("saturacion-oxigeno/<int:paciente_id>/", views.saturacion_oxigeno, name="saturacion_oxigeno"),
    path("disnea/<int:paciente_id>/", views.disnea, name="disnea"),

    #Topbar

    path("mensajeria/<int:paciente_id>/", views.mensajeria, name="mensajeria"),
    path("mensajeria/nuevo/<int:paciente_id>/", views.nuevo_mensaje, name="nuevo_mensaje"),
    path("consultas-gestiones/<int:paciente_id>/", views.consultas_gestiones, name="consultas_gestiones"),

    #Sidebar
    
    path("estudios/<int:paciente_id>/", views.estudios, name="estudios"),
    path("estudios/cargar/<int:paciente_id>/", views.cargar_estudio, name="cargar_estudio"),
    path("medicamentos/<int:paciente_id>/", views.medicamentos, name="medicamentos"),
    path("mis-medicos/<int:paciente_id>/", views.mis_medicos, name="mis_medicos"),
    path("teleconsultas/<int:paciente_id>/", views.teleconsultas, name="teleconsultas"),
    path("cartilla/<int:paciente_id>/", views.cartilla, name="cartilla"),
    path("mi-diario/<int:paciente_id>/", views.mi_diario, name="mi_diario"),
]

