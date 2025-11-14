from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = "usuarios"

class UsuarioLoginView(LoginView):
    template_name = "usuarios/login.html"

urlpatterns = [
    path("login/", UsuarioLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="usuarios:login"), name="logout"),
    path("perfil/", views.perfil_usuario, name="perfil"),
    path("registrar_custom/", views.registrar_usuario, name="registrar"),
    path("paciente/<int:pk>/", views.detalle_paciente_usuario, name="detalle_paciente"),
    path("crear-paciente/", views.crear_paciente, name="crear_paciente"),
]
