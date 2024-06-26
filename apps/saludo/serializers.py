from rest_framework import serializers
from .models import saludo




class saludoSerializer(serializers.ModelSerializer):


	class Meta:

		model = saludo
		fields = ('pk_publica','mensaje' ) 

	def __str__(self):

		return self.saludoSerializer