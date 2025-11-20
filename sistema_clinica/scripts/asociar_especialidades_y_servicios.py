import random
from profesionales.models import Profesional, Especialidad, Servicio

especialidades = list(Especialidad.objects.all())
servicios = list(Servicio.objects.all())
profesionales = Profesional.objects.all()

for profesional in profesionales:

    profesional.especialidad = random.choice(especialidades)

    #(ManyToMany)
    num_serv = random.randint(1, 3)
    serv_random = random.sample(servicios, num_serv)

    profesional.servicios.clear()
    profesional.servicios.add(*serv_random)

    profesional.save()

    print(f"✔ {profesional.nombre} asignado a {profesional.especialidad.nombre} "
          f"con {num_serv} servicios")
