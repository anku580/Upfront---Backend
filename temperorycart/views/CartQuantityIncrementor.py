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

class CartQuantityIncrementor(APIView):
	def post(self,request):

		# menuname = request.data['item']
		customList = request.data['customId']
		try:
			go = Cart.objects.get(itemId = request.data['itemId'],user =request.user.id)
			# resposeDict['status'] = 'item already exist in the cart'
		
			menuObj = Menu . objects.get(id = request.data['itemId'])

		
			# request.data['itemId'] = menuObj.id
			# del request.data['item']
			print('requestDict',request.data)
			serializer =QuantityIncrementSerializer(data=request.data)

			if serializer.is_valid(raise_exception=ValueError):
				obj1 = Cart.objects.get(itemId=serializer.data['itemId'],user = request.user.id)
				# print(obj1,serializer.data['quantity'],obj1.quantity)
				obj1.quantity += serializer.data['quantity']
				obj1.save()
	
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
							cartMenuCustomObj1 = CartMenuCustomization.objects.get(id = j.id)
							cartMenuCustomObj1.quantity +=  serializer.data['quantity']
							cartMenuCustomObj1.save()
					if checkStatus == False:
						cartMenuCustomObj = CartMenuCustomization(menu_id = menuObj, customUser = request.user, cartNo = go, quantity =  serializer.data['quantity'])
						cartMenuCustomObj.save()
						for i in customList:
							# menuObj = Menu.objects.get(id = request.data['itemId'])
							customObj = Customization.objects.get(id = i)
							menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['itemId'],customization_id = i)
							customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
							customQuantityObj.save()
						return Response({"status":"item added to the cartObj and customization applied"}) 




					
					# cartMenuCustomObj.save()
					# customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
					# customQuantityObj.save()
					return Response({"status":"item added to the cartObj and customization quantity increased"}) 
				except Customization.DoesNotExist:
					return Response({"error":"no such customisations exist"}, status=status.HTTP_404_NOT_FOUND)
				except Menu.DoesNotExist:
					return Response({"error":"no such Menu exist"}, status=status.HTTP_404_NOT_FOUND)
				except MenuCustomization.DoesNotExist:
					return Response({"error":"no such Customization  exist for this particular menu"}, status=status.HTTP_404_NOT_FOUND)
				except CartMenuCustomization.DoesNotExist:
					cartMenuCustomObj = CartMenuCustomization(menu_id = menuObj, customUser = request.user, cartNo = go, quantity = serializer.data['quantity'])
					cartMenuCustomObj.save()
					for i in customList:
							menuObj = Menu.objects.get(id = request.data['itemId'])
							customObj = Customization.objects.get(id = i)
							menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['itemId'],customization_id = i)
							customQuantityObj = CustomizationOnQuantity(cartMenuId = cartMenuCustomObj, customId =customObj)
							customQuantityObj.save()
					# cartMenuCustomObj.customization.add(customObj)
					# cartMenuCustomObj.save()

			return Response({"status":"item added to the cartObj and customization applied"}) 
		except Cart.DoesNotExist:
			return Response({"status":"item not present in cart"})

