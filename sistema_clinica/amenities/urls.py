from django.urls import path
from . import views

app_name = "amenities"

urlpatterns = [
    path("<int:paciente_id>/gimnasio/", views.gimnasio, name="gimnasio"),
    path("<int:paciente_id>/nutricion/", views.nutricion, name="nutricion"),
    path("<int:paciente_id>/talleres/", views.talleres, name="talleres"),
]
