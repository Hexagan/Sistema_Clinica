from django.db import models
from pacientes.models import Paciente

class Amenity(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

class UsoAmenity(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    antes_del_turno = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = "Uso de Amenity"
        verbose_name_plural = "Usos de Amenities"

