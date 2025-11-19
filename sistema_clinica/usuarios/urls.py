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
    path("portal-paciente/<int:paciente_id>/", views.portal_paciente, name="portal_paciente")
]
