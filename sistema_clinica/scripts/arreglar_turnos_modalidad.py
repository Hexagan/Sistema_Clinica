from turnos.models import Turno
from profesionales.models import Profesional
from django.db import transaction

@transaction.atomic
def run():
    print("=== Ajustando modalidades de turnos ===")

    nuevos = []
    eliminados = []

    turnos = Turno.objects.select_related("profesional").all()

    for t in turnos:
        tipo = t.profesional.tipo_consulta

        # PROFESIONAL SOLO PRESENCIAL
        if tipo == "PRES":
            t.modalidad = "PRES"
            t.save()
            continue

        # PROFESIONAL SOLO TELECONSULTA
        if tipo == "TELE":
            t.modalidad = "TELE"
            t.save()
            continue

        # PROFESIONAL HÍBRIDO (AMBOS)
        if tipo == "AMBOS":

            # si ya existe un turno TELE o PRES para este intervalo, evitar duplicación
            existe_pres = Turno.objects.filter(
                profesional=t.profesional,
                fecha=t.fecha,
                hora=t.hora,
                modalidad="PRES"
            ).exists()

            existe_tele = Turno.objects.filter(
                profesional=t.profesional,
                fecha=t.fecha,
                hora=t.hora,
                modalidad="TELE"
            ).exists()

            # si el turno actual no está asignado → lo convertimos en PRES
            t.modalidad = "PRES"
            t.save()

            # crear TELE si no existe
            if not existe_tele:
                Turno.objects.create(
                    profesional=t.profesional,
                    fecha=t.fecha,
                    hora=t.hora,
                    modalidad="TELE",
                    estado=t.estado,
                )
                nuevos.append((t.fecha, t.hora, t.profesional.nombre))

    print(f"✔ Turnos TELE creados para híbridos: {len(nuevos)}")
    print("Proceso completado.")
