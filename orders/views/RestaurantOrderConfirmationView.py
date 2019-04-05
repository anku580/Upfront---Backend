from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.views.generic import View 
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator
from payment import Checksum
from temperorycart.models import Order, Cart,TotalCost,PermanentCart
from menu_app.models import Menu
import base64
import json
import datetime
import pytz
from restaurant_app.models import Restaurant
from myuser.models import MyUser

import cgi


class RestaurantOrderConfirmationView(APIView):
	permission_class = (AllowAny)


	def get(self,request,pk=None,resId =None):
		errorDict = {}
		totalcost = 0
		itemscost = 0
		ResponseDict = {}
		TotalCostObj = TotalCost(Totalcost=-1)
		TotalCostObj.save()
		orderNo = TotalCostObj.id
		restaurants = {}
		i = 0
		restaurantItems ={}
		print('runnu=ing')
		while i >= 0:
			try:

				cartObj = Cart.objects.filter(user=request.user.id)[i]
				
			except IndexError:
				if i == 0:
					if errorDict == {}:
						errorDict['No_Cart_Items'] ='your cart is empty'
				if errorDict:
					# TotalCostObj.delete()

					return Response(errorDict)
				# Timeline = namedtuple('Timeline', ('items', 'totalCost'))
				# TotalCostObj.Totalcost=totalcost
				# TotalCostObj.save()
			
				print("restaurants:",restaurantItems)
				# for i in restaurants.keys():

					# OrderObj.orderRestaurants.add(Restaurant.objects.get(id = i))
					# billObj = BillModel(orderNo = TotalCostObj,billuser = request.user,billResId =(Restaurant.objects.get(id = i)),Cost = restaurants[i] )
					# billObj.save()

				# timeline = Timeline(items =PermanentCart.objects.filter(orderNo=TotalCostObj.id),totalCost=TotalCost.objects.filter(id=TotalCostObj.id),)
				# serializer = CompleteOrderSerializer(timeline)
				# print(serializer.data
				# 	)
				tz = pytz.timezone('Asia/Kolkata')
				currentDT = datetime.datetime.now(tz)
					


				restaurantItems["time"] =  currentDT.strftime("%I:%M:%S %p")
				if resId == None:
					return Response(restaurantItems)
				else:
					resObj = Restaurant.objects.get(id = resId)
					if resObj.name not in restaurantItems.keys():
						return Response({'error':'no items of restaurant in cart'})
					restaurantItems[resObj.name].update(time =  currentDT.strftime("%I:%M:%S %p"),orderNo= 1 )
					return Response(restaurantItems[resObj.name])
			print('requestTest1',request.user.id)
			CartObj = Cart.objects.filter(user=request.user.id)[i]
			print(CartObj)
			MenuObj = Menu.objects.get(id = CartObj.items.id)
			print(MenuObj.res_id.name)
			# if MenuObj.res_id.id not in restaurants.keys():
			# 	restaurants[MenuObj.res_id.id] = 0
			if MenuObj.res_id.name not in restaurantItems.keys():
				restaurantItems[MenuObj.res_id.name] = {} #creating a dictionary for having item quantity pair.

		
			if(MenuObj.quantity<CartObj.quantity):

				errorDict[MenuObj.name]=MenuObj.name + " has only "+str(MenuObj.quantity) + " remaining"
				CartObj1 = Cart.objects.get(items = CartObj.items.id,user=request.user.id)
				CartObj1.delete()
				
			else:
				# print('testing else')
				# itemscost  = MenuObj.price*CartObj.quantity 
				restaurantItems[MenuObj.res_id.name][MenuObj.name] = cartObj.quantity
				# restaurants[MenuObj.res_id.id] += itemscost
				# totalcost += itemscost
			
				# MenuObj.quantity -= CartObj.quantity
				Myobj = MyUser.objects.get(id =request.user.id)
			
				PermanentCartObj = PermanentCart(orderNo = TotalCostObj,Cartuser = Myobj,Cartitems = MenuObj,  itemsCost= itemscost,quantity = CartObj.quantity )
				PermanentCartObj.save()

				# MenuObj.save()
				# CartObj1 = Cart.objects.get(items = CartObj.items.id,user=request.user.id)
				# CartObj1.delete()
			i  = i + 1

		 
		return Response({'error':'error occured'})

	def post( self,request ):
		orderNoList = request.data['orderNo']
		print(orderNoList)
		return Response({'orderNo' : orderNoList})




