from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from temperorycart.models import Cart
from temperorycart.serializers import CartSerializer, QuantityIncrementSerializer
from menu_app.models import Menu
from customization_app.models import Customization, MenuCustomization
from temperorycart.models import CartMenuCustomization, CustomizationOnQuantity




class CartQuantityDecrementor(APIView):
	def post(self,request):
		customList = request.data['customId']
		# menuname = request.data['items']
		# menuObj = Menu . objects.get(name = menuname)

	
		# request.data['itemId'] = menuObj.id
		try:
			go = Cart.objects.get(itemId = request.data['itemId'],user =request.user.id)
			menuObj = Menu . objects.get(id = request.data['itemId'])

			serializer =QuantityIncrementSerializer(data=request.data)
			if serializer.is_valid(raise_exception=ValueError):
				obj1 = Cart.objects.get(itemId = serializer.data['itemId'], user = request.user.id)
				
				print(obj1,serializer.data['quantity'],obj1.quantity)
				if customList:
					try:
						checkStatus = False
						go = Cart.objects.get(itemId = request.data['itemId'],user =request.user.id)
						cartMenuCustomObj = CartMenuCustomization.objects.filter(menu_id = request.data['itemId'], customUser = request.user.id, cartNo = go.id)
						menuObj = Menu.objects.get(id = request.data['itemId'])
						# customObj = Customization.objects.get(id = i)
						# menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['itemId'],customization_id = i)
						for j in cartMenuCustomObj:
							customQuantityObj = CustomizationOnQuantity.objects.filter(cartMenuId = j.id)
							checkList =[]
							for k in customQuantityObj:
								checkList.append(k.customId.id)

							if set(customList) == set(checkList):
								checkStatus = True
								cartMenuCustomObj1 = CartMenuCustomization.objects.get(id= j.id)
								if(cartMenuCustomObj1.quantity >=  serializer.data['quantity']):
									cartMenuCustomObj1.quantity -=  serializer.data['quantity']
									cartMenuCustomObj1.save()
								if(cartMenuCustomObj1.quantity ==  serializer.data['quantity']):
									cartMenuCustomObj1.delete()
						if checkStatus == False:
							# cartMenuCustomObj = CartMenuCustomization(menu_id = menuObj, customUser = request.user, cartNo = go, quantity =  serializer.data['quantity'])
							# cartMenuCustomObj.save()
							# for i in customList:
							# 	# menuObj = Menu.objects.get(id = request.data['itemId'])
							# 	customObj = Customization.objects.get(id = i)
							# 	menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['itemId'],customization_id = i)
							# 	customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
							# 	customQuantityObj.save()
							return Response({"status":"item with given customization is not added to the cart"}) 




						
						# cartMenuCustomObj.save()
						# customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
						# customQuantityObj.save()
						# return Response({"status":"item added to the cartObj and customization quantity increased"}) 
					except Customization.DoesNotExist:
						return Response({"error":"no such customisations exist"}, status=status.HTTP_404_NOT_FOUND)
					except Menu.DoesNotExist:
						return Response({"error":"no such Menu exist"}, status=status.HTTP_404_NOT_FOUND)
					except MenuCustomization.DoesNotExist:
						return Response({"error":"no such Customization  exist for this particular menu"}, status=status.HTTP_404_NOT_FOUND)
					except CartMenuCustomization.DoesNotExist:
						# cartMenuCustomObj = CartMenuCustomization(menu_id = menuObj, customUser = request.user, cartNo = go, quantity = serializer.data['quantity'])
						# cartMenuCustomObj.save()
						# for i in customList:
						# 		menuObj = Menu.objects.get(id = request.data['itemId'])
						# 		customObj = Customization.objects.get(id = i)
						# 		menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['itemId'],customization_id = i)
						# 		customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
						# 		customQuantityObj.save()
						# # cartMenuCustomObj.customization.add(customObj)
						# # cartMenuCustomObj.save()
						return Response({"error":"items with the given customization does not exist"})

			 
				if (obj1.quantity <= serializer.data['quantity']):
					obj1.delete()
					return Response({"status": "item removed from cart"})
				else:
					obj1.quantity -= serializer.data['quantity']
					obj1.save()

					return Response({'itemId':menuObj.id,'itemName':menuObj.name,'current quantity of item':obj1.quantity})
			return Response({"status": "failed"})
		except Cart.DoesNotExist:
			return Response({"status":"item not present in cart"})



 