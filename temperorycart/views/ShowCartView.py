from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action


from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from temperorycart.models import Cart
from customization_app.models import Customization, MenuCustomization
from menu_app.models import Menu
from temperorycart.models import CartMenuCustomization, CustomizationOnQuantity

from temperorycart.serializers import CartSerializer, QuantityIncrementSerializer

class CartViewSet(APIView):
	def post(self, request, pk=None):
		print(request.user.id)
		request.data['user'] = request.user.id
		resposeDict = {}
		customList = request.data['customId']
		# menuname = request.data['item']
		# menuObj = Menu . objects.get(name = menuname)

		# print(menuObj.id)
		# request.data['itemId'] = menuObj.id
		try:
			go = Cart.objects.get(itemId = request.data['itemId'],user =request.user.id)
			# resposeDict['status'] = 'item already exist in the cart'
		
		except Cart.DoesNotExist:
		


			serializer = CartSerializer(data=request.data)
			if serializer.is_valid():
				go = None
				serializer.save()

				print('customlist',customList)
				if customList:
					try:
						cartMenuCustomObj = CartMenuCustomization.objects.get(menu_id = request.data['itemId'], customUser = request.user.id, cartNo = go)
						return Response({"error":"cart"})
					except CartMenuCustomization.DoesNotExist:
						for i in customList:
							try:
								customObj = Customization.objects.get(id = i)
								go = Cart.objects.get(itemId = request.data['itemId'],user =request.user.id)
								menuObj = Menu.objects.get(id = request.data['itemId'])
								menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['itemId'],customization_id = i)
								cartMenuCustomObj = CartMenuCustomization.objects.get(menu_id = request.data['itemId'], customUser = request.user.id, cartNo = go)
								cartMenuCustomObj.save()
								customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
								customQuantityObj.save()
								return Response({"status":"item added to the cartObj and customization quantity increased"}) 
							except Customization.DoesNotExist:
								return Response({"error":"no such customisations exist"}, status=status.HTTP_404_NOT_FOUND)
							except Menu.DoesNotExist:
								return Response({"error":"no such Menu exist"}, status=status.HTTP_404_NOT_FOUND)
							except MenuCustomization.DoesNotExist:
								return Response({"error":"no such Customization  exist for this particular menu"}, status=status.HTTP_404_NOT_FOUND)
							except CartMenuCustomization.DoesNotExist:
								cartMenuCustomObj = CartMenuCustomization(menu_id = menuObj, customUser = request.user, quantity = serializer.data['quantity'], cartNo = go)
								cartMenuCustomObj.save()
								customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
								customQuantityObj.save()
								# cartMenuCustomObj.customization.add(customObj)
								# cartMenuCustomObj.save()

						return Response({"status":"item added to the cartObj and customization applied"}) 

				return Response({'status': 'item added to the cartObj'})
			else:
			    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		return Response({"error":"item already in the cart"},status=status.HTTP_400_BAD_REQUEST)
	def get(self,request, pk = None):
		cartObj = Cart.objects.filter(user = request.user.id)
		serializer = CartSerializer(cartObj,many = True,context = {"totalcost":request})
		print(serializer.data)
		newDict ={}
		totalcost = 0
		for i in serializer.data:
			itemcost = 0 
			newDict[i['id']]={}
			# print(i['itemId'])
			menuObj = Menu.objects.get(id = i['itemId'])
			itemcost = menuObj.discounted_price * i['quantity']
			print('price',menuObj.original_price)
			i['itemName'] = menuObj.name
			i['user'] = request.user.username
			i['customization'] = {}
			i['no_customization'] = {}
			count  = 0
			customQuantity = 0
			cartMenuCustomObj = CartMenuCustomization.objects.filter(cartNo = i['id'])
			for  j in cartMenuCustomObj:
				count += 1
				tempList= []
				cost = 0
				totalCustomCost = 0
				customQuantityObj = CustomizationOnQuantity.objects.filter(cartMenuId = j.id)
				for k in  customQuantityObj:
					tempList.append(k.customId.name)
					cost += k.customId.price

				# print(j.customization.all())
				# for  k in j.customization.all():
				# 	print(k.name)
					# 	tempstr += k.name + ','
				i['customization']['customization_' + str(count)] = {} 
				i['customization']['customization_' + str(count)]['customisations_applied'] = tempList
				i['customization']['customization_' + str(count)]['quantity'] = j.quantity
				customQuantity += j.quantity
				# if tempstr not in i['customization'].keys():
				# 	i['customization'][tempstr] = 1
				# else:
				# 	i['customization'][tempstr] += 1


				
				i['customization']['customization_' + str(count)]['cutomizationCost'] =cost * j.quantity
				i['customization']['customization_' + str(count)]['cutomizedItemCost'] = (cost+menuObj.discounted_price)*j.quantity 
				cost *= j.quantity
				itemcost += cost
				i['itemcost'] = itemcost
			totalcost += itemcost
			i['no_customization']['noCustomizationAppliedQuantity'] = i['quantity'] - customQuantity
			i['no_customization']['cost'] = (i['quantity'] - customQuantity) * menuObj.discounted_price
			newDict[i['id']].update(i)
		newDict['totalcost'] = totalcost

		print('newDict' ,newDict)

		return Response(newDict)
