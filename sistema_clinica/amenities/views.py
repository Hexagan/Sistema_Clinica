from django.shortcuts import render
from pacientes.models import Paciente
from .models import Amenity, Beneficio

def cargar_paciente(request, paciente_id):
    perfil = request.user.perfil
    return perfil.pacientes.get(pk=paciente_id)

def gimnasio(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    amenity = Amenity.objects.get(nombre="Gimnasio")
    beneficios = amenity.beneficios.filter(activo=True)
    return render(request, "amenities/gimnasio.html", {
        "paciente": paciente,
        "amenity": amenity,
        "beneficios": beneficios,
    })


def kiosco(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    amenity = Amenity.objects.get(nombre="Kiosco y Nutrición")
    beneficios = amenity.beneficios.filter(activo=True)
    return render(request, "amenities/kiosco.html", {
        "paciente": paciente,
        "amenity": amenity,
        "beneficios": beneficios,
    })


def nutricion(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    amenity = Amenity.objects.get(nombre="Relajación y Mindfulness")
    beneficios = amenity.beneficios.filter(activo=True)
    return render(request, "amenities/nutricion.html", {
        "paciente": paciente,
        "amenity": amenity,
        "beneficios": beneficios,
    })


def talleres(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    amenity = Amenity.objects.get(nombre="Talleres y Asesoramiento de Salud")
    beneficios = amenity.beneficios.filter(activo=True)
    return render(request, "amenities/talleres.html", {
        "paciente": paciente,
        "amenity": amenity,
        "beneficios": beneficios,
    })

