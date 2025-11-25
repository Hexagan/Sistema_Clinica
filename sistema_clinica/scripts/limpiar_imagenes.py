from profesionales.models import Profesional
from django.conf import settings
import os

def run():
    print("=== LIMPIEZA DE IMÁGENES DE PROFESIONALES ===")

    media_folder = os.path.join(settings.MEDIA_ROOT, "profesionales")

    # Todas las imágenes actualmente asignadas a profesionales
    usadas = set(
        os.path.basename(p.foto.name)
        for p in Profesional.objects.exclude(foto="")
        if p.foto and p.foto.name
    )

    print("Imágenes actualmente usadas:")
    print(usadas)

    # Todas las imágenes que existen físicamente en la carpeta media/profesionales/
    if not os.path.isdir(media_folder):
        print("Carpeta no encontrada:", media_folder)
        return

    existentes = set(os.listdir(media_folder))

    print("Imágenes encontradas físicamente:")
    print(existentes)

    # Sobran = existen pero no las usa ningún profesional
    sobrantes = existentes - usadas

    print("\nImágenes sobrantes detectadas:")
    print(sobrantes)

    if not sobrantes:
        print("No hay imágenes para eliminar.")
        return

    confirm = input("\n¿Eliminar estas imágenes sobrantes? (s/n): ").lower().strip()

    if confirm != "s":
        print("Cancelado.")
        return

    # Eliminación
    for img in sobrantes:
        path = os.path.join(media_folder, img)
        try:
            os.remove(path)
            print(f"Eliminada: {img}")
        except Exception as e:
            print(f"ERROR eliminando {img}: {e}")

    print("\nProceso de limpieza completado.")
