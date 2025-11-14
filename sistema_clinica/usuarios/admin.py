from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "telefono", "direccion")
    search_fields = ("user__username", "user__email")
    ordering = ("user__username",)
