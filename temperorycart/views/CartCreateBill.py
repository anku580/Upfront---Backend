from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from temperorycart.models import Cart, PermanentCart, TotalCost , Order, BillModel
from menu_app.models import Menu
from restaurant_app.models import Restaurant
from myuser.models import MyUser 
from customization_app.models import Customization, MenuCustomization
from temperorycart.models import CartMenuCustomization, CustomizationOnQuantity
from temperorycart.serializers import CartSerializer, QuantityIncrementSerializer,CompleteOrderSerializer
from collections import namedtuple

import datetime
import pytz

class CartCreateBill(APIView):

	def get(self,request,pk=None):
		               
		errorDict = {}
		totalcost = 0
		itemscost = 0
		
		ResponseDict = {}
		TotalCostObj = TotalCost(Totalcost=-1)
		TotalCostObj.save()
		restaurants = {}
		restaurantItems = {}
		newDict = {}
		while True:
			try: 

				cartObj = Cart.objects.filter(user=request.user.id)[0]
				
			except IndexError:
				if totalcost == 0:
					if errorDict == {}:
						errorDict['No_Cart_Item'] ='your cart is empty'
				if errorDict:
					TotalCostObj.delete()

					return Response(errorDict)
				Timeline = namedtuple('Timeline', ('items', 'totalCost'))
				TotalCostObj.Totalcost=totalcost
				TotalCostObj.save()
				tz = pytz.timezone('GMT')
				currentDT = datetime.datetime.now(tz)
				currentDT  = currentDT + datetime.timedelta(hours=5,minutes = 30) 
				
 
				OrderObj = Order(orderUser = request.user,Payment_type = 1,orderNo = TotalCostObj, totalcost = TotalCostObj.Totalcost,orderCreatedTime = currentDT) 
				OrderObj.save()
				print("restaurants:",restaurantItems)
				for i in restaurants.keys():

					# OrderObj.orderRestaurants.add(Restaurant.objects.get(id = i))
					billObj = BillModel(orderNo = TotalCostObj,billuser = request.user,billResId =(Restaurant.objects.get(id = i)),Cost = restaurants[i] )
					billObj.save()

				timeline = Timeline(items =PermanentCart.objects.filter(orderNo=TotalCostObj.id),totalCost=TotalCost.objects.filter(id=TotalCostObj.id),)
				serializer = CompleteOrderSerializer(timeline)

				print(serializer.data
					)

				newDict =serializer.data
				newDict['orderNo'] = TotalCostObj.id
				newDict['cartUser'] = request.user.username
				newDict['cartUserId']  = request.user.id

				for i in newDict['items']:
					menuNameObj = Menu.objects.get(id = i['cartItem'] )
					i['cartItemName'] = menuNameObj.name
					i['cartItemId'] = i['cartItem']
					del i['cartItem']
					del i["orderNo"]
					del i["cartUser"]

				print('newDict = ',newDict)
				return Response(newDict)
			print('requestTest1',request.user.id)
			CartObj = Cart.objects.filter(user=request.user.id)[0]
			print(CartObj)
			MenuObj = Menu.objects.get(id = CartObj.itemId.id)
			print(MenuObj.res_id.id)
			if MenuObj.res_id.id not in restaurants.keys():
				restaurants[MenuObj.res_id.id] = 0
			if MenuObj.res_id.id not in restaurantItems.keys():
				restaurantItems[MenuObj.res_id.id] = {} #creating a dictionary for having item quantity pair.

		
			if(MenuObj.quantity<CartObj.quantity):

				errorDict[MenuObj.name]=MenuObj.name + " has only "+str(MenuObj.quantity) + " remaining"
				CartObj1 = Cart.objects.get(itemId = CartObj.itemId.id,user=request.user.id)
				CartObj1.delete()
				
			else:
				print('testing else')
				itemscost  = MenuObj.discounted_price*CartObj.quantity 
				restaurantItems[MenuObj.res_id.id][MenuObj.name] = cartObj.quantity
				restaurants[MenuObj.res_id.id] += itemscost
				cartMenuCustomObj = CartMenuCustomization.objects.filter(menu_id = MenuObj.id, customUser = request.user.id, cartNo = CartObj.id)
				for customMenu in  cartMenuCustomObj:
					customCost = 0
					customQuantityObj = CustomizationOnQuantity.objects.filter(cartMenuId = customMenu.id)
					for customQuantity in customQuantityObj:
						customCost += customQuantity.customId.price
					customCost *= customMenu.quantity
					itemscost += customCost
					print('customCost',customCost)

					print(itemscost)
				totalcost += itemscost

				MenuObj.quantity -= CartObj.quantity
				Myobj = MyUser.objects.get(id =request.user.id)
			
				PermanentCartObj = PermanentCart(orderNo = TotalCostObj,cartUser = Myobj,cartItem = MenuObj,  itemCost= itemscost,quantity = CartObj.quantity )
				PermanentCartObj.save()

				MenuObj.save()
				CartObj1 = Cart.objects.get(itemId = CartObj.itemId.id,user=request.user.id)
				CartObj1.delete()
 