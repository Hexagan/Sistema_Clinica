# turnos/scripts/limpiar_turnos_modalidad_erronea.py

from turnos.models import Turno


def run(*args):
    """
    Ejecutar con:
        python manage.py runscript limpiar_turnos_modalidad_erronea
    """

    print("Buscando turnos con modalidad incorrecta...")

    turnos = Turno.objects.select_related("profesional").filter(
        paciente__isnull=True
    )

    eliminados = 0

    for turno in turnos:

        tipo_prof = turno.profesional.tipo_consulta
        modalidad_turno = turno.modalidad

        eliminar = False

        if tipo_prof == "PRES" and modalidad_turno == "TELE":
            eliminar = True

        elif tipo_prof == "TELE" and modalidad_turno == "PRES":
            eliminar = True

        # AMBOS no se toca

        if eliminar:
            turno.delete()
            eliminados += 1

    print(f"✔ Se eliminaron {eliminados} turnos con modalidad incorrecta.")