from datetime import datetime, timedelta
from django.utils import timezone
from turnos.models import Turno, Estado
from profesionales.models import Profesional

DIAS_MAP = {
    "Lun": 0, "Mar": 1, "Mie": 2, "Jue": 3,
    "Vie": 4, "Sab": 5, "Dom": 6
}

def run(*args):
    """
    Ejecutar con:
        python manage.py runscript generar_turnos --script-args 30 20
    """

    dias = int(args[0]) if len(args) > 0 else 30
    intervalo = int(args[1]) if len(args) > 1 else 30

    estado_pendiente = Estado.objects.get(pk=1)
    hoy = timezone.localdate()

    print("Generando turnos...")

    profesionales = Profesional.objects.filter(estado=True)

    for profesional in profesionales:

        if not profesional.dias_disponibles:
            continue

        dias_prof = profesional.dias_disponibles.split("-")
        dias_indices = [DIAS_MAP[d] for d in dias_prof if d in DIAS_MAP]

        inicio = profesional.horario_inicio
        fin = profesional.horario_fin

        if not inicio or not fin:
            continue

        fecha_actual = hoy

        for _ in range(dias):

            if fecha_actual.weekday() in dias_indices:

                dt_inicio = datetime.combine(fecha_actual, inicio)
                dt_fin = datetime.combine(fecha_actual, fin)
                slot_dt = dt_inicio

                while slot_dt < dt_fin:
                    hora = slot_dt.time()

                    modalidades = []

                    if profesional.tipo_consulta == "PRES":
                        modalidades = ["PRES"]

                    elif profesional.tipo_consulta == "TELE":
                        modalidades = ["TELE"]

                    elif profesional.tipo_consulta == "AMBOS":
                        modalidades = ["PRES", "TELE"]

                    for modalidad in modalidades:

                        existe = Turno.objects.filter(
                            profesional=profesional,
                            fecha=fecha_actual,
                            hora=hora,
                            modalidad=modalidad
                        ).exists()

                        if not existe:
                            Turno.objects.create(
                                profesional=profesional,
                                fecha=fecha_actual,
                                hora=hora,
                                estado=estado_pendiente,
                                modalidad=modalidad
                            )

                    slot_dt += timedelta(minutes=intervalo)

            fecha_actual += timedelta(days=1)

    print("✔ Turnos generados correctamente según modalidad.")
