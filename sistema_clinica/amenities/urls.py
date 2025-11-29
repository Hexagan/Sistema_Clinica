from django.urls import path
from .views import (
    GimnasioView,
    KioscoView,
    NutricionView,
    TalleresView,
)

app_name = "amenities"

urlpatterns = [
    path("gimnasio/<int:paciente_id>/", GimnasioView.as_view(), name="gimnasio"),
    path("nutricion/<int:paciente_id>/", NutricionView.as_view(), name="nutricion"),
    path("talleres/<int:paciente_id>/", TalleresView.as_view(), name="talleres"),
    path("kiosco/<int:paciente_id>/", KioscoView.as_view(), name="kiosco"),
]
