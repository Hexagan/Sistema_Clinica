from django.urls import path
from .views import lista_servicios

app_name = "servicios"

urlpatterns = [
    path('', lista_servicios, name='lista_servicios'), 
]
