from django.db import models
from pacientes.models import Paciente
from profesionales.models import Profesional
from servicios.models import Servicio


class Estado(models.Model):
    descripcion = models.CharField(max_length=50)


class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    fecha = models.DateField()
    hora = models.TimeField()
    piso = models.CharField(max_length=10) 
    qr_code = models.CharField(max_length=200, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

