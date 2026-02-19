from django.utils import timezone
from datetime import datetime
from turnos.models import Turno


def run(*args):

    ahora = timezone.localtime()

    print("Buscando turnos vencidos sin paciente...")

    turnos = Turno.objects.filter(paciente__isnull=True)

    eliminados = 0

    for turno in turnos:
        dt_turno = timezone.make_aware(
            datetime.combine(turno.fecha, turno.hora)
        )

        if dt_turno < ahora:
            turno.delete()
            eliminados += 1

    print(f"✔ Se eliminaron {eliminados} turnos vencidos sin paciente.")