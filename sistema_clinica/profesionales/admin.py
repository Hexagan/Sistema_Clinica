from django.contrib import admin
from .models import Profesional, Especialidad, Servicio

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
    list_display = ("nombre", "email", "matricula", "estado", "especialidad", "mostrar_servicios")
    list_filter = ("estado", "especialidad", "servicios")
    search_fields = ("nombre", "email", "matricula")
    filter_horizontal = ("servicios",)

    def mostrar_servicios(self, obj):
        return ", ".join(s.nombre for s in obj.servicios.all())

    mostrar_servicios.short_description = "Servicios"