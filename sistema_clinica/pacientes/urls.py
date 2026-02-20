from django.urls import path

# Importar cada módulo de views
from pacientes.views.portal import PortalPacienteView
from pacientes.views.dashboard import (
    PacienteDetalleView,
    ListaPacientesView,
    CrearPacienteView,
    CreacionPacienteExitosaView
)
from pacientes.views.controles import (
    IndicacionesView,
    PesoAlturaView,
    TemperaturaView,
    FrecuenciaCardiacaView,
    PresionArterialView,
    GlucemiaView,
    FrecuenciaRespiratoriaView,
    SaturacionOxigenoView,
    DisneaView
)
from pacientes.views.mensajeria import (
    MensajeriaView,
    NuevoMensajeView,
    MensajeDetalleView
)
from pacientes.views.estudios import (
    EstudiosView,
    CargarEstudioView
)
from pacientes.views.otros import (
    CoberturaMedicaView,
    MedicamentosView,
    MisMedicosView,
    TeleconsultasView,
    MiDiarioView,
    ConsultasGestionesView
)

app_name = "pacientes"

urlpatterns = [
    # ======================
    #   PORTAL + PACIENTES
    # ======================
    path("<int:paciente_id>/", PortalPacienteView.as_view(), name="portal_paciente"),
    path("paciente/<int:pk>/", PacienteDetalleView.as_view(), name="paciente_detalle"),
    path("crear/", CrearPacienteView.as_view(), name="crear_paciente"),
    path("creacion-exitosa/", CreacionPacienteExitosaView.as_view(), name="creacion_paciente_exitosa"),
    path("lista/", ListaPacientesView.as_view(), name="lista_pacientes"),

    # ======================
    #   CONTROLES
    # ======================
    path("indicaciones/<int:paciente_id>/", IndicacionesView.as_view(), name="indicaciones"),
    path("peso-altura/<int:paciente_id>/", PesoAlturaView.as_view(), name="peso_altura"),
    path("temperatura/<int:paciente_id>/", TemperaturaView.as_view(), name="temperatura"),
    path("frecuencia-cardiaca/<int:paciente_id>/", FrecuenciaCardiacaView.as_view(), name="frecuencia_cardiaca"),
    path("presion-arterial/<int:paciente_id>/", PresionArterialView.as_view(), name="presion_arterial"),
    path("glucemia/<int:paciente_id>/", GlucemiaView.as_view(), name="glucemia"),
    path("frecuencia-respiratoria/<int:paciente_id>/", FrecuenciaRespiratoriaView.as_view(), name="frecuencia_respiratoria"),
    path("saturacion-oxigeno/<int:paciente_id>/", SaturacionOxigenoView.as_view(), name="saturacion_oxigeno"),
    path("disnea/<int:paciente_id>/", DisneaView.as_view(), name="disnea"),

    # ======================
    #   MENSAJERÍA
    # ======================
    path("mensajeria/<int:paciente_id>/", MensajeriaView.as_view(), name="mensajeria"),
    path("mensajeria/nuevo/<int:paciente_id>/", NuevoMensajeView.as_view(), name="nuevo_mensaje"),
    path("mensajeria/<int:paciente_id>/<int:mensaje_id>/", MensajeDetalleView.as_view(), name="mensaje_detalle"),

    # ======================
    #   ESTUDIOS
    # ======================
    path("estudios/<int:paciente_id>/", EstudiosView.as_view(), name="estudios"),
    path("estudios/cargar/<int:paciente_id>/", CargarEstudioView.as_view(), name="cargar_estudio"),

    # ======================
    #   OTROS
    # ======================
    path("medicamentos/<int:paciente_id>/", MedicamentosView.as_view(), name="medicamentos"),
    path("mis-medicos/<int:paciente_id>/", MisMedicosView.as_view(), name="mis_medicos"),
    path("teleconsultas/<int:paciente_id>/", TeleconsultasView.as_view(), name="teleconsultas"),
    path("cartilla/<int:paciente_id>/", MisMedicosView.as_view(), name="cartilla"),  # O si existe CartillaView, cámbialo
    path("mi-diario/<int:paciente_id>/", MiDiarioView.as_view(), name="mi_diario"),
    path("consultas-gestiones/<int:paciente_id>/", ConsultasGestionesView.as_view(), name="consultas_gestiones"),
    path("cobertura/<int:paciente_id>/", CoberturaMedicaView.as_view(), name="cobertura_medica"
)

]
