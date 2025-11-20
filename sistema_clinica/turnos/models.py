from django.db import models
from pacientes.models import Paciente
from profesionales.models import Profesional, Servicio


class Estado(models.Model):
    descripcion = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.descripcion


class Turno(models.Model):
    paciente = models.ForeignKey(
        'pacientes.Paciente',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE
    )

    estado = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        default=1          
    )

    fecha = models.DateField()
    hora = models.TimeField()

    qr_code = models.CharField(max_length=200, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.profesional}"
