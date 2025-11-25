from django.shortcuts import render, redirect, get_object_or_404
from pacientes.models import Paciente
from datetime import date, datetime

from .models import (
    PesoAltura, Temperatura, FrecuenciaCardiaca, PresionArterial,
    Glucemia, FrecuenciaRespiratoria, Disnea, SaturacionOxigeno, Indicaciones
)


# ----------------------------------------  
# Utilidad común
# ----------------------------------------
def get_paciente(paciente_id):
    return get_object_or_404(Paciente, id=paciente_id)

# ----------------------------------------
# 1. Peso y altura
# ----------------------------------------
def peso_altura(request, paciente_id):
    paciente = get_paciente(paciente_id)

    # Traer el último registro real por fecha + hora
    ultimo = PesoAltura.objects.filter(
        paciente_id=paciente_id
    ).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        PesoAltura.objects.create(
            paciente_id=paciente_id,
            altura=float(request.POST["altura"]),
            peso=float(request.POST["peso"]),
            fecha=request.POST["fecha"],
            # hora se autogenera
        )
        return redirect("controles:peso_altura", paciente_id=paciente_id)

    return render(request, "controles/peso_altura.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })

# ----------------------------------------
# 2. Temperatura
# ----------------------------------------
def temperatura(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = Temperatura.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"

        Temperatura.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            zona=request.POST.get("zona"),
            fecha=fecha_str,
            hora=hora_con_segundos
            
        )
        return redirect("controles:temperatura", paciente_id=paciente_id)

    return render(request, "controles/temperatura.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 3. Frecuencia cardiaca
# ----------------------------------------
def frecuencia_cardiaca(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = FrecuenciaCardiaca.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"

        FrecuenciaCardiaca.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            metodo=request.POST["metodo"],
            fecha=fecha_str,
            hora=hora_con_segundos   # ahora tiene hh:mm:ss
        )
        return redirect("controles:frecuencia_cardiaca", paciente_id=paciente_id)

    return render(request, "controles/frecuencia_cardiaca.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 4. Presión arterial
# ----------------------------------------
def presion_arterial(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = PresionArterial.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"

        PresionArterial.objects.create(
            paciente_id=paciente_id,
            alta=request.POST["alta"],
            baja=request.POST["baja"],
            zona=request.POST["zona"],
            tensiometro=request.POST["tensiometro"],
            tomado_por=request.POST["tomado_por"],
            fecha=fecha_str,
            hora=hora_con_segundos
        )
        return redirect("controles:presion_arterial", paciente_id=paciente_id)

    return render(request, "controles/presion_arterial.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 5. Glucemia
# ----------------------------------------
def glucemia(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = Glucemia.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"

        Glucemia.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            post_comida=request.POST["post_comida"],
            fecha=fecha_str,
            hora=hora_con_segundos
        )
        return redirect("controles:glucemia", paciente_id=paciente_id)

    return render(request, "controles/glucemia.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 6. Frecuencia respiratoria
# ----------------------------------------
def frecuencia_respiratoria(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = FrecuenciaRespiratoria.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"
        FrecuenciaRespiratoria.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            fecha=fecha_str,
            hora=hora_con_segundos
        )
        return redirect("controles:frecuencia_respiratoria", paciente_id=paciente_id)

    return render(request, "controles/frecuencia_respiratoria.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 7. Disnea
# ----------------------------------------
def disnea(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = Disnea.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"
        
        Disnea.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            fecha=fecha_str,
            hora=hora_con_segundos
        )
        return redirect("controles:disnea", paciente_id=paciente_id)

    return render(request, "controles/disnea.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 8. Saturación de oxígeno
# ----------------------------------------
def saturacion_oxigeno(request, paciente_id):
    paciente = get_paciente(paciente_id)
    ultimo = SaturacionOxigeno.objects.filter(paciente_id=paciente_id).order_by('-fecha', '-hora').first()

    if request.method == "POST":
        fecha_str = request.POST["fecha"]
        hora_str = request.POST["hora"]

        ahora = datetime.now()
        hora_con_segundos = hora_str + f":{ahora.second:02d}"
        SaturacionOxigeno.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            oxigeno_suplementario=request.POST.get("oxigeno_suplementario") == "si",
            fecha=fecha_str,
            hora=hora_con_segundos
        )
        return redirect("controles:saturacion_oxigeno", paciente_id=paciente_id)

    return render(request, "controles/saturacion_oxigeno.html", {
        "ultimo": ultimo,
        "paciente": paciente,
        "today": date.today(),
        "now": datetime.now(),
    })


# ----------------------------------------
# 9. Indicaciones / Piezas de información
# ----------------------------------------
def indicaciones(request, paciente_id):
    paciente = get_paciente(paciente_id)
    piezas = Indicaciones.objects.filter(activo=True).order_by('-fecha')

    return render(request, "controles/indicaciones.html", {
        "piezas": piezas,
        "paciente": paciente
    })
