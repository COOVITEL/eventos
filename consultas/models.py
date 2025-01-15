from django.db import models

class EntregaObsequio(models.Model):
    nombre = models.CharField(max_length=200)
    documento = models.CharField(max_length=200)
    sucursal = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    obsequio = models.CharField(max_length=200)
    asesor = models.CharField(max_length=200)
    razonDeEntrega = models.CharField(max_length=1000, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
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