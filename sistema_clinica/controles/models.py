# controles/models.py
from django.db import models
from pacientes.models import Paciente


class PesoAltura(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    altura = models.FloatField()  # en metros
    peso = models.FloatField()    # en kg
    fecha = models.DateField()
    imc = models.FloatField(null=True, blank=True)

    def calcular_imc(self):
        if self.altura > 0:
            self.imc = round(self.peso / (self.altura ** 2), 2)
        else:
            self.imc = None
        return self.imc

    def save(self, *args, **kwargs):
        self.calcular_imc()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Peso y Altura"
        verbose_name_plural = "Pesos y Alturas"


class Temperatura(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.FloatField()
    zona = models.CharField(max_length=20)  # axilar/boca/rectal/etc.
    fecha = models.DateField()
    hora = models.TimeField()


class FrecuenciaCardiaca(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    metodo = models.CharField(max_length=20)  # manual/automatico
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        verbose_name = "Frecuencia Cardíaca"
        verbose_name_plural = "Frecuencias Cardíacas"

class PresionArterial(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    alta = models.PositiveIntegerField()
    baja = models.PositiveIntegerField()
    zona = models.CharField(max_length=20)  # brazo/muñeca
    tensiometro = models.CharField(max_length=20)  # manual/automatico
    tomado_por = models.CharField(max_length=50)
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        verbose_name = "Presión Arterial"
        verbose_name_plural = "Presiones Arteriales"

class Glucemia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    post_comida = models.CharField(max_length=5)  # si/no
    fecha = models.DateField()
    hora = models.TimeField()


class FrecuenciaRespiratoria(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        verbose_name = "Frecuencia Respiratoria"
        verbose_name_plural = "Frecuencias Respiratorias"

class Disnea(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()  # escala 0 a 10
    fecha = models.DateField()
    hora = models.TimeField()

class SaturacionOxigeno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()  # en %
    oxigeno_suplementario = models.BooleanField()
    fecha = models.DateField()
    hora = models.TimeField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.valor}% - {self.fecha}"
    
    class Meta:
        verbose_name = "Saturación de Oxígeno"
        verbose_name_plural = "Saturaciones de Oxígeno"

class Indicaciones(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Indicación"
        verbose_name_plural = "Indicaciones"