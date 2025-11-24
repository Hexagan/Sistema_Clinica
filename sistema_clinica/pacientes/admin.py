from django.contrib import admin
from .models import Paciente, Mensaje, Estudio

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "dni", "telefono", "perfil_usuario")
    search_fields = ("nombre", "apellido", "dni")
    list_filter = ("perfil_usuario",)
    ordering = ("nombre",)

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ("id", "remitente", "profesional_destino", "creado", "leido")
    list_filter = ("leido", "creado", "profesional_destino")
    search_fields = ("texto", "remitente__username", "profesional_destino__nombre")
    ordering = ("-creado",)
    readonly_fields = ("creado",)

    actions = ["marcar_como_leidos"]

    def marcar_como_leidos(self, request, queryset):
        queryset.update(leido=True)
    marcar_como_leidos.short_description = "Marcar mensajes seleccionados como leídos"

@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "fecha_estudio", "creado", "tiene_archivo")
    list_filter = ("fecha_estudio", "creado")
    search_fields = ("paciente__nombre", "paciente__apellido")
    ordering = ("-fecha_estudio",)

    def tiene_archivo(self, obj):
        return bool(obj.archivo)
    tiene_archivo.boolean = True
    tiene_archivo.short_description = "Archivo"

