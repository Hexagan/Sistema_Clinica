from django.urls import path
from .views import (
    UsuarioLoginView, RegistrarUsuarioView, PerfilUsuarioView,
    PacienteDetalleUsuarioView
)
from django.contrib.auth.views import LogoutView

app_name = "usuarios"

urlpatterns = [
    path("login/", UsuarioLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="usuarios:login"), name="logout"),
    path("registrar_custom/", RegistrarUsuarioView.as_view(), name="registrar"),
    path("perfil/", PerfilUsuarioView.as_view(), name="perfil"),
    path("paciente/<int:pk>/",
         PacienteDetalleUsuarioView.as_view(), name="detalle_paciente"),
]
