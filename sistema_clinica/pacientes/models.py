from django.db import models

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

