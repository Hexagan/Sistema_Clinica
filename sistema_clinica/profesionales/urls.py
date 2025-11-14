from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_profesionales, name='lista_profesionales'),
    path('<int:profesional_id>/', views.detalle_profesional, name='detalle_profesional'),
    path('especialidades/', views.lista_especialidades, name='lista_especialidades'),
]
