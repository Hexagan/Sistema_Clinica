from django.urls import path
from .views import lista_amenities

urlpatterns = [
    path('', lista_amenities, name='lista_amenities'),
]
