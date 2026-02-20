from django.db import models
from pacientes.models import Paciente
from turnos.models import Turno

class Amenity(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Amenities"

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


class Beneficio(models.Model):
    """
    Un beneficio concreto asociado a un Amenity.
    Ej: '1 sesión gratis de 30 min', 'Descuento 20% en la primera clase', 'Snack saludable gratuito', etc.
    """
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="beneficios")
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    # opcional: límite de entregas, validez, etc.
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.amenity.nombre} - {self.titulo}"

class BeneficioOtorgado(models.Model):
    """
    Registro de un beneficio otorgado a un paciente por un turno (al llegar temprano).
    """
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, related_name="beneficios_otorgados")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="beneficios_recibidos")
    beneficio = models.ForeignKey(Beneficio, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    notificado = models.BooleanField(default=False)  # para tracking si ya se envío notificación

    def __str__(self):
        return f"{self.paciente} - {self.beneficio} @ {self.timestamp}"

    class Meta:
        verbose_name = "Beneficio Otorgado"
        verbose_name_plural = "Beneficios Otorgados"