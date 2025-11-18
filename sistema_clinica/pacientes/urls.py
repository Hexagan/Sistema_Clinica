from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.portal_paciente, name="portal_paciente"),
    path("paciente/<int:pk>/", views.paciente_detalle, name="paciente_detalle"),
    path('crear_paciente/', views.crear_paciente, name='crear_paciente'),
    path("creacion_paciente_exitosa/", views.creacion_paciente_exitosa, name="creacion_paciente_exitosa"),
    path("lista_pacientes/", views.lista_pacientes, name="lista_pacientes"),
]
