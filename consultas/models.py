from django.db import models
from django.utils import timezone


class EntregaObsequio(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=200)
    sucursal = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    obsequio = models.CharField(max_length=200)
    asesor = models.CharField(max_length=200)
    razonDeEntrega = models.CharField(max_length=1000, blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nombre} - {self.documento} - {self.fecha}"

class Asesor(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nombre}"

class Sucursal(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre}"

class Asociado(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    causa = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nombre}"
