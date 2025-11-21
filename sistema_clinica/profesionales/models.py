from django.db import models


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    
    def __str__(self):
        return self.nombre

class Profesional(models.Model):

    TIPO_CONSULTA = [
    ('PRES', 'Presencial'),
    ('TELE', 'Teleconsulta'),
    ('AMBOS', 'Hibrida'),
    ]
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    foto = models.ImageField(upload_to='profesionales/', null=True, blank=True)
    estado = models.BooleanField(default=True)
    
    servicios = models.ManyToManyField(Servicio, blank=True)
    disponibilidad = models.CharField(max_length=200)
    piso = models.IntegerField()
    consultorio = models.CharField(max_length=20, blank=True, null=True)
    horario_inicio = models.TimeField(blank=True, null=True)
    horario_fin = models.TimeField(blank=True, null=True)
    dias_disponibles = models.CharField(max_length=100, blank=True, null=True)
    tipo_consulta = models.CharField(max_length=5, choices=TIPO_CONSULTA, default='PRES')

    def dias_como_lista(self):
        if not self.dias_disponibles:
            return []
        return [d.strip() for d in self.dias_disponibles.split("-")]

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name='profesionales'
    )

    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"

    def __str__(self):
        return self.nombre + " - " + self.especialidad.nombre
