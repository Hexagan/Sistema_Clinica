from django.urls import path
from .views import lista_turnos

urlpatterns = [
    path('', lista_turnos, name='lista_turnos'),
]
