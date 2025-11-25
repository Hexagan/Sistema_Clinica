from django.urls import path
from . import views

app_name = "amenities"

urlpatterns = [
    path("gimnasio/<int:paciente_id>/", views.gimnasio, name="gimnasio"),
    path("nutricion/<int:paciente_id>", views.nutricion, name="nutricion"),
    path("talleres/<int:paciente_id>/", views.talleres, name="talleres"),
    path('kiosco/<int:paciente_id>/', views.kiosco, name='kiosco'),
]
