from django.urls import path
from .views import  saludoAPI, saludo1API




urlpatterns = [
	path('', saludo1API.as_view(), name="saludoAPI"),
	path('<pk_publica>/', saludoAPI.as_view(), name="saludoAPIact"),
]