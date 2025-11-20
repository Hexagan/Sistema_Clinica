import random
from profesionales.models import Profesional

def run():
    TIPOS = ["PRES", "TELE", "AMBOS"]

    count = 0
    for p in Profesional.objects.all():
        p.tipo_consulta = random.choice(TIPOS)
        p.save(update_fields=["tipo_consulta"])
        count += 1

    print(f"Actualizados {count} profesionales.")
