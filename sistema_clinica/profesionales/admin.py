from django.contrib import admin
from .models import Profesional, Especialidad, Servicio
from django.utils.html import format_html

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)
    
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "email", "matricula", "estado", "especialidad",
        "mostrar_servicios", "dias_disponibles", "horario_inicio",
        "horario_fin", "tipo_consulta", "consultorio", "piso",
        "foto_preview",
    )
    list_filter = ("estado", "especialidad", "servicios")
    search_fields = ("nombre", "email", "matricula")
    filter_horizontal = ("servicios",)

    def mostrar_servicios(self, obj):
        return ", ".join(s.nombre for s in obj.servicios.all())
    mostrar_servicios.short_description = "Servicios"

    # Mostrar miniatura
    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover; border-radius:4px;" />',
                obj.foto.url
            )
        return "—"
    foto_preview.short_description = "Foto"