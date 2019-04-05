from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from temperorycart.models import Cart, PermanentCart, TotalCost , Order
from menu_app.models import Menu
from myuser.models import MyUser 
from temperorycart.serializers import CartSerializer, QuantityIncrementSerializer,OrderSerializer
from collections import namedtuple



class CartCreateOrder(APIView):

	
	def put(self,request,pk=None):
		obj1 = Order.objects.get(orderNo = pk,Orderuser= request.user.id,Status=1 )
		serializer = OrderSerializer(obj1,data=request.data)
		if serializer.is_valid(raise_exception=ValueError):
			
			serializer.save()
		
			return Response(serializer.data)
		return Response({"status": "failed"})
	def get(self,request,pk=None):
		
		serializer = OrderSerializer(obj1,data=request.data)
		if serializer.is_valid(raise_exception=ValueError):
			
			serializer.save()
		
			return Response(serializer.data)
		return Response({"status": "failed"})