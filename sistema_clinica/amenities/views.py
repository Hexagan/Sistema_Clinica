from django.shortcuts import render
from django.shortcuts import get_object_or_404
from pacientes.models import Paciente

def cargar_paciente(request, paciente_id):
    perfil = request.user.perfil
    return perfil.pacientes.get(pk=paciente_id)

def gimnasio(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "amenities/gimnasio.html", {
        "paciente": paciente,
        "paciente_id": paciente_id
    })

def nutricion(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "amenities/nutricion.html", {
        "paciente": paciente,
        "paciente_id": paciente_id
    })

def talleres(request, paciente_id):
    paciente = cargar_paciente(request, paciente_id)
    return render(request, "amenities/talleres.html", {
        "paciente": paciente,
        "paciente_id": paciente_id
    })
