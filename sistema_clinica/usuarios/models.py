from django.db import models
from django.contrib.auth.models import User
from pacientes.models import Paciente
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    # Relación: un usuario puede gestionar varios pacientes
    pacientes = models.ManyToManyField(Paciente, related_name="responsables", blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


# Crear automáticamente un perfil cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
