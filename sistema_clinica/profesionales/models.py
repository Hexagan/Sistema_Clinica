from django.db import models
from servicios.models import Servicio

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)


class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    foto = models.ImageField(upload_to='profesionales/', null=True, blank=True)
    estado = models.BooleanField(default=True)  # activo/inactivo

    disponibilidad = models.CharField(max_length=200)
    consultorio = models.CharField(max_length=20, blank=True, null=True)
    horario_inicio = models.TimeField(blank=True, null=True)
    horario_fin = models.TimeField(blank=True, null=True)
    dias_disponibles = models.CharField(max_length=100, blank=True, null=True)

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name='profesionales'
    )

    servicios = models.ManyToManyField(
        Servicio,
        related_name='profesionales',
        blank=True
    )

