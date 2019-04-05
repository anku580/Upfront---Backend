from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Testing(APIView):
	def get (self, request):
		context ={
		"message": "testing successfull"
		}
		return Response(context)
