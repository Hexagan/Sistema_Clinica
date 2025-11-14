from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "telefono", "direccion")
    search_fields = ("usuario__username", "usuario__email")
    ordering = ("usuario__username",)
