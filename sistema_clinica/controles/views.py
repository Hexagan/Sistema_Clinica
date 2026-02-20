# controles/views.py

from datetime import datetime, date
from django.shortcuts import render, redirect
from django.views import View

from pacientes.mixins import PacienteAccessMixin
from pacientes.models import Paciente

from .models import (
    PesoAltura, Temperatura, FrecuenciaCardiaca,
    PresionArterial, Glucemia, FrecuenciaRespiratoria,
    Disnea, SaturacionOxigeno, Indicaciones
)

class PesoAlturaView(PacienteAccessMixin, View):
    template_name = "controles/peso_altura.html"
    model = PesoAltura
    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })
    
    def post(self, request, paciente_id):
        PesoAltura.objects.create(
            paciente_id=paciente_id,
            altura=float(request.POST["altura"]),
            peso=float(request.POST["peso"]),
            fecha=request.POST["fecha"]
        )
        return redirect("controles:peso_altura", paciente_id=paciente_id)


class TemperaturaView(PacienteAccessMixin, View):
    template_name = "controles/temperatura.html"
    model = Temperatura
    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })

    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        Temperatura.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            zona=request.POST.get("zona"),
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:temperatura", paciente_id=paciente_id)


class FrecuenciaCardiacaView(PacienteAccessMixin, View):
    template_name = "controles/frecuencia_cardiaca.html"
    model = FrecuenciaCardiaca
    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })

    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        FrecuenciaCardiaca.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            metodo=request.POST["metodo"],
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:frecuencia_cardiaca", paciente_id=paciente_id)


class PresionArterialView(PacienteAccessMixin, View):
    template_name = "controles/presion_arterial.html"
    model = PresionArterial
    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })

    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        PresionArterial.objects.create(
            paciente_id=paciente_id,
            alta=request.POST["alta"],
            baja=request.POST["baja"],
            zona=request.POST["zona"],
            tensiometro=request.POST["tensiometro"],
            tomado_por=request.POST["tomado_por"],
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:presion_arterial", paciente_id=paciente_id)


class GlucemiaView(PacienteAccessMixin, View):
    template_name = "controles/glucemia.html"
    model = Glucemia
    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })

    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        Glucemia.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            post_comida=request.POST["post_comida"],
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:glucemia", paciente_id=paciente_id)


class FrecuenciaRespiratoriaView(PacienteAccessMixin, View):
    template_name = "controles/frecuencia_respiratoria.html"
    model = FrecuenciaRespiratoria

    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })
    
    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        FrecuenciaRespiratoria.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:frecuencia_respiratoria", paciente_id=paciente_id)


class DisneaView(PacienteAccessMixin, View):
    template_name = "controles/disnea.html"
    model = Disnea

    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })

    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        Disnea.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:disnea", paciente_id=paciente_id)


class SaturacionOxigenoView(PacienteAccessMixin, View):
    template_name = "controles/saturacion_oxigeno.html"
    model = SaturacionOxigeno
    
    def get(self, request, paciente_id):
        paciente = self.get_paciente()

        ultimo = self.model.objects.filter(
            paciente_id=paciente_id
        ).order_by("-fecha", "-hora").first()

        return render(request, self.template_name, {
            "ultimo": ultimo,
            "paciente": paciente,
            "today": date.today(),
            "now": datetime.now(),
        })
    
    def post(self, request, paciente_id):
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        ahora = datetime.now()

        SaturacionOxigeno.objects.create(
            paciente_id=paciente_id,
            valor=request.POST["valor"],
            oxigeno_suplementario=request.POST.get("oxigeno_suplementario") == "si",
            fecha=fecha,
            hora=f"{hora}:{ahora.second:02d}"
        )
        return redirect("controles:saturacion_oxigeno", paciente_id=paciente_id)


class IndicacionesView(PacienteAccessMixin, View):
    template_name = "controles/indicaciones.html"

    def get(self, request, paciente_id):
        paciente = self.get_paciente()
        piezas = Indicaciones.objects.filter(activo=True).order_by("-fecha")

        return render(request, self.template_name, {
            "piezas": piezas,
            "paciente": paciente
        })
