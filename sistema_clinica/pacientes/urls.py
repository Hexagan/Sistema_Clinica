from django.urls import path
from .views import lista_pacientes, detalle_paciente

urlpatterns = [
    path('', lista_pacientes, name='lista_pacientes'),
    path('<int:paciente_id>/', detalle_paciente, name='detalle_paciente'),
]
