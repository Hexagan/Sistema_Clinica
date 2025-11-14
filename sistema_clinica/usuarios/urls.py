from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("registrar/", views.registrar_usuario, name="registrar"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("perfil/", views.perfil_usuario, name="perfil"),
    path("pacientes/nuevo/", views.crear_paciente, name="crear_paciente"),
    path("paciente/<int:pk>/", views.detalle_paciente_usuario, name="paciente_detalle"),
]
