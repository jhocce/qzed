from django.shortcuts import render
import json
# Create your views here.
from django.db.models import Q, F
from ast import literal_eval
from django.http import Http404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .ManageApi import ErrorManagerMixin
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.core.paginator import Paginator

from .serializers import saludoSerializer
from .models import saludo



class saludoAPI(ErrorManagerMixin, ListAPIView, 
	RetrieveAPIView, UpdateAPIView, DestroyAPIView, APIView):
	
	serializer_class = saludoSerializer
	model = saludo
	
	def update(self, request,pk_publica=None, *arg, **kwargs):
		"""Enviar por get el "pk_public" del cliente a quien se le actualizara una sucursal """
		try:
			if pk_publica is None:
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar la sucursal',
				mensaje_server='No se a enviado correctamente la variable "pk_public" correspondiente al objeto a actualizar en la URL', status='error')
				return Response(self.salida(), status=400)
			else:
				try:				
					objeto = self.model.objects.get(pk_publica=pk_publica, 
						Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = 'Ocurrieron uno o mas errores a actualizar el saludo',
						mensaje_server = 'El objeto no existe o no pertenece al usuario al que esta relacionado al token')
					return Response(self.salida(), status=404)
				
				serviciosSerializer = self.serializer_class( objeto, data= request.data)
				if serviciosSerializer.is_valid():
				
					serviciosSerializer.save()
					self.MensajeListAdd(mensaje_user='El saludo a sido guardada con exito', status='success')
					self.JsonAdd(json = serviciosSerializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = serviciosSerializer.errors )
					self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de actualizar el saludo',
						mensaje_server=serviciosSerializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def get(self, request, pk_publica=None, *arg, **kwargs):
		""" Enviar por get con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
		 de todos los registros del usuario en cuestion de ser asi enviar: \n
		    count: numero de elmentos por pagina \n
		    page: numero de pagina """
		try:
		
			if pk_publica is None:

				# quey = self.get_queryset()
				
				query =  self.model.objects.filter(Status=True)
				total_count = query.count()
				if self.count and self.page:
					paginacion= Paginator(query,self.count)
					
					if len(paginacion.page(1)) == 0:
						
						pass
					else:
						query= paginacion.page(self.page)
				if query is not None and total_count!=0:
					
					total_count = query.object_list.count()
					f = self.serializer_class(query, many=True)
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
				else:
					self.JsonAdd(json={
						"total_count":0,
						"data":[]
						})
					self.MensajeListAdd(mensaje_user = 'No hay registros')
				return Response(self.salida(), status=200)
			else:
				
					
				query =  self.model.objects.get(Status=True, pk_publica=pk_publica)
				if query is None:
					self.MensajeListAdd(mensaje_user = 'El saludo no existe no existe',
						mensaje_server = 'El saludo no existe')			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

	def delete(self, request,pk_publica=None, *arg, **kwargs):
		
		try:
			objeto = self.model.objects.get(pk_publica=pk_publica)
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = 'La sucursal a sido eliminado exitosamente')
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			
		

		return Response(self.salida(), status=200)

class saludo1API(ErrorManagerMixin,CreateAPIView, APIView):
	def dispatch(self, request, *args, **kwargs):
		self.count = request.GET.get('count')
		self.page = request.GET.get('page')
		if self.count==None:
			self.count=100
		if self.page==None:
			self.page=1
		return super().dispatch(request, *args, **kwargs)
	
	serializer_class = saludoSerializer
	model = saludo
	def post(self, request, *arg, **kwargs):
		""" Enviar por body los datos del saludo a guardar  """
		
		        
		try:
			serviciosSerializer = self.serializer_class(data= request.data)
			
			
			if serviciosSerializer.is_valid():
				serviciosSerializer.save()
				self.MensajeListAdd(mensaje_user='Saludo Guardada Exitosamente', status='success')
	
				data = dict(serviciosSerializer.data)
				self.JsonAdd(json = data )
				return Response( self.salida(), status=200)

			else:
				
				self.JsonAdd(json = serviciosSerializer.errors )
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el saludo',
					mensaje_server=serviciosSerializer.errors, status='error')
				return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el saludo', mensaje_server  = str(e))
			return Response(self.salida(), status=500)
	def get(self, request, pk_publica=None, *arg, **kwargs):
		""" Enviar por get con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
		 de todos los registros del usuario en cuestion de ser asi enviar: \n
		    count: numero de elmentos por pagina \n
		    page: numero de pagina """
		try:
		
			if pk_publica is None:

				# quey = self.get_queryset()
				
				query =  self.model.objects.filter(Status=True)
				print(query)
				total_count = query.count()
				if self.count and self.page:
					
					paginacion= Paginator(query,self.count)
					
					if len(paginacion.page(1)) == 0:
						
						pass
					else:
						query= paginacion.page(self.page)
				if query is not None and total_count!=0:
					
					total_count = query.object_list.count()
					f = self.serializer_class(query, many=True)
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
				else:
					self.JsonAdd(json={
						"total_count":0,
						"data":[]
						})
					self.MensajeListAdd(mensaje_user = 'No hay registros')
				return Response(self.salida(), status=200)
			else:
				
					
				query =  self.model.objects.get(Status=True, pk_publica=self.pk_publica)
				if query is None:
					self.MensajeListAdd(mensaje_user = 'El saludo no existe no existe',
						mensaje_server = 'El saludo no existe')			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)