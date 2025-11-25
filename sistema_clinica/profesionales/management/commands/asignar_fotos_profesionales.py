import os
from django.core.management.base import BaseCommand
from profesionales.models import Profesional
from django.core.files import File

class Command(BaseCommand):
    help = "Asigna automáticamente fotos a los profesionales según Dr o Dra"

    def handle(self, *args, **kwargs):
        base_path = "static/img/profesionales"

        carpeta_dr = os.path.join(base_path, "dr")
        carpeta_dra = os.path.join(base_path, "dra")

        # Obtener listas de imágenes ordenadas
        fotos_dr = sorted(f for f in os.listdir(carpeta_dr) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
        fotos_dra = sorted(f for f in os.listdir(carpeta_dra) if f.lower().endswith(('.jpg', '.jpeg', '.png')))

        idx_dr = 0
        idx_dra = 0

        for profesional in Profesional.objects.all():
            nombre = profesional.nombre.strip().lower()

            if nombre.startswith("dr."):
                if idx_dr < len(fotos_dr):
                    foto_path = os.path.join(carpeta_dr, fotos_dr[idx_dr])
                    idx_dr += 1
                else:
                    self.stdout.write(self.style.WARNING(f"NO quedan fotos para hombres"))
                    continue

            elif nombre.startswith("dra."):
                if idx_dra < len(fotos_dra):
                    foto_path = os.path.join(carpeta_dra, fotos_dra[idx_dra])
                    idx_dra += 1
                else:
                    self.stdout.write(self.style.WARNING(f"NO quedan fotos para mujeres"))
                    continue
            else:
                self.stdout.write(self.style.ERROR(f"Nombre sin Dr/Dra: {profesional.nombre}"))
                continue

            with open(foto_path, "rb") as f:
                profesional.foto.save(os.path.basename(foto_path), File(f), save=True)

            self.stdout.write(self.style.SUCCESS(
                f"Asignada {os.path.basename(foto_path)} a {profesional.nombre}"
            ))

        self.stdout.write(self.style.SUCCESS("Asignación completada"))
