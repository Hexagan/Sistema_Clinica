from django.db import models
from django.contrib.auth.models import User
from pacientes.models import Paciente

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    pacientes = models.ManyToManyField(Paciente, related_name="responsables", blank=True)     # Relación: un usuario puede gestionar varios pacientes

    def __str__(self):
        return f"{self.usuario.username} (ID {self.id})"


