from django.core.management.base import BaseCommand
from amenities.models import Amenity, Beneficio
from datetime import time

# -----------------------------------------
# CONFIGURACIÓN DE AMENITIES + BENEFICIOS
# -----------------------------------------

AMENITIES = {
    "Gimnasio": {
        "descripcion": "Acceso al gimnasio con máquinas, pesas y clases",
        "horario_apertura": time(7, 0),
        "horario_cierre": time(21, 0),
        "beneficios": [
            ("Entrada gratuita 1 día", "Acceso gratis al gimnasio por un día."),
            ("Clase grupal sin cargo", "Participación gratuita en clase colectiva."),
            ("Evaluación física inicial", "Evaluación rápida con instructor."),
            ("Descuento del 20% en plan mensual", "Promoción para nuevos usuarios."),
            ("Acceso prioritario", "Pasar sin esperar en recepción del gym."),
        ],
    },

    "Talleres y Asesoramiento de Salud": {
        "descripcion": "Charlas, talleres y asesorías con especialistas",
        "horario_apertura": time(9, 0),
        "horario_cierre": time(18, 0),
        "beneficios": [
            ("Entrada gratis a un taller", "Vale por un taller a elección."),
            ("2x1 para el próximo taller", "Promoción válida 1 mes."),
            ("Material didáctico gratuito", "Incluye cuadernillo digital."),
            ("Descuento del 10% en talleres", "Para cualquier inscripción futura."),
            ("Asesoría breve de salud", "Miniconsulta de 10 minutos."),
        ],
    },

    "Relajación y Mindfulness": {
        "descripcion": "Espacios de meditación, respiración y bienestar",
        "horario_apertura": time(8, 0),
        "horario_cierre": time(20, 0),
        "beneficios": [
            ("Clase express de mindfulness", "Sesión guiada de 20 minutos."),
            ("Acceso a sala de relajación", "Pase gratuito por 1 hora."),
            ("Audio de meditación", "Descarga de meditación guiada."),
            ("Descuento en pack de sesiones", "Descuento del 15%."),
            ("Infusión relajante", "Bebida herbal incluida."),
        ],
    },

    "Kiosco y Nutrición": {
        "descripcion": "Espacio con snacks saludables y consejos rápidos",
        "horario_apertura": time(8, 0),
        "horario_cierre": time(22, 0),
        "beneficios": [
            ("Snack saludable gratis", "Barra de cereal o fruta."),
            ("Bebida natural sin cargo", "Infusión o jugo natural."),
            ("Descuento del 10% en compras", "Aplicable a un ticket."),
            ("Consejo nutricional breve", "Recomendación de un nutricionista."),
            ("Cupón de merchandising", "Descuento en productos saludables."),
        ],
    },

    "Taller": {
        "descripcion": "Gimnasio orientado a rehabilitación y movilidad",
        "horario_apertura": time(10, 0),
        "horario_cierre": time(16, 0),
        "beneficios": [
        ("Entrada a taller gratis", "Acceso a un taller de interés."),
        ("2x1 en taller", "Promoción 2x1 en la próxima sesión."),
        ("Materiales gratuitos", "Se entregan materiales para el taller."),
        ("Descuento en inscripción", "10% de descuento para próximas inscripciones."),
        ("Cupón regalo", "Cupón para invitar a un acompañante.")
        ],
    },
}


# -----------------------------------------------------
# COMANDO PRINCIPAL
# -----------------------------------------------------

class Command(BaseCommand):
    help = "Crea amenities y beneficios predeterminados con horarios coherentes."

    def handle(self, *args, **kwargs):

        for nombre, data in AMENITIES.items():
            amenity, creado = Amenity.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": data["descripcion"],
                    "costo": 0,
                    "horario_apertura": data["horario_apertura"],
                    "horario_cierre": data["horario_cierre"],
                    "disponible": True,
                }
            )

            if creado:
                self.stdout.write(self.style.SUCCESS(f"Amenity creado: {nombre}"))
            else:
                # Si ya existe, aseguramos que tenga horarios para evitar errores en modelos viejos
                cambios = False
                if amenity.horario_apertura is None:
                    amenity.horario_apertura = data["horario_apertura"]
                    cambios = True
                if amenity.horario_cierre is None:
                    amenity.horario_cierre = data["horario_cierre"]
                    cambios = True
                if cambios:
                    amenity.save()
                    self.stdout.write(self.style.WARNING(f"Amenity {nombre} actualizado con horarios."))

            # ---------------------------
            # CREAR BENEFICIOS
            # ---------------------------

            for titulo, desc in data["beneficios"]:
                beneficio, creado_b = Beneficio.objects.get_or_create(
                    amenity=amenity,
                    titulo=titulo,
                    defaults={
                        "descripcion": desc,
                        "activo": True
                    }
                )

                if creado_b:
                    self.stdout.write(self.style.SUCCESS(f"  Beneficio creado: {titulo}"))
                else:
                    self.stdout.write(f"  Beneficio ya existe: {titulo}")

        self.stdout.write(self.style.SUCCESS("Carga de amenities y beneficios completada."))
