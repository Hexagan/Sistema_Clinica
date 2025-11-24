from django.db import models
from django.conf import settings

class Paciente(models.Model):

    perfil_usuario = models.ForeignKey(
        'usuarios.PerfilUsuario',
        on_delete=models.CASCADE,
        related_name="pacientes_asociados"
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    email = models.EmailField()
    telefono = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    obra_social = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre + " " + self.apellido
    
class Mensaje(models.Model):
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mensajes_enviados"
    )

    profesional_destino = models.ForeignKey(
        'profesionales.Profesional',
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos'
    )

    texto = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creado']


    def __str__(self):
        return (
            f"Mensaje {self.id} — "
            f"{self.remitente.username} → {self.profesional_destino.nombre}"
        )

class Estudio(models.Model):
    paciente = models.ForeignKey(
        'pacientes.Paciente',
        on_delete=models.CASCADE,
        related_name='estudios'
    )

    fecha_estudio = models.DateField()
    observaciones = models.TextField(blank=True)

    archivo = models.FileField(
        upload_to='estudios/',
        blank=True,
        null=True
    )

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_estudio', '-creado']

    def __str__(self):
        return f"Estudio {self.id} - {self.paciente} ({self.fecha_estudio})"
    