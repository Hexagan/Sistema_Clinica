from django.shortcuts import render
from django.http import HttpResponse

def lista_pacientes(request):
    return HttpResponse("Listado de pacientes")

def detalle_paciente(request, paciente_id):
    return HttpResponse(f"Detalle del paciente {paciente_id}")
