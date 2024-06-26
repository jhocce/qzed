import uuid
from django.db import models

# Create your models here.
class basemodel(models.Model):

	""" Modelo astracto que se hereda en todos lo modelos que existen dentro del sistema
	 contiene conlumnas que son genericas para cualquier registro en la BD """
	Creado = models.DateTimeField(auto_now_add=True)
	Modificado =models.DateTimeField(auto_now=True)
	Status = models.BooleanField(default=True)
	pk_publica = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	Codigo = models.CharField(max_length=60, blank=True, null=True)
	

	class Meta:
		""" Declaracion de abstración para el modelo basemodel """
		abstract = True

class saludo(basemodel):
	
    mensaje = models.CharField(max_length=300)