from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from customization_app.models import Customization, MenuCustomization
from menu_app.models import Menu
from temperorycart.models import CartMenuCustomization
class CustomizationMenu(APIView):

	def post(self,request):
		for i in request.data['customId']:
			try:
				customObj = Customization.objects.get(id = i)
				menuObj = Menu.objects.get(id = request.data['menuId'])
				menuCustomObj = MenuCustomization.objects.get(menu_id = request.data['menuId'],customization_id = i)
				cartMenuCustomObj = CartMenuCustomization.objects.get(customization = i,menu_id = request.data['menuId'], customUser = request.user.id)
				cartMenuCustomObj.quantity += 1
				cartMenuCustomObj.save()
				return Response({"status":"customization quantity increased"}) 
			except Customization.DoesNotExist:
				return Response({"error":"no such customisations exist"}, status=status.HTTP_404_NOT_FOUND)
			except Menu.DoesNotExist:
				return Response({"error":"no such Menu exist"}, status=status.HTTP_404_NOT_FOUND)
			except MenuCustomization.DoesNotExist:
				return Response({"error":"no such Customization  exist for this particular menu"}, status=status.HTTP_404_NOT_FOUND)
			except CartMenuCustomization.DoesNotExist:
				cartMenuCustomObj = CartMenuCustomization(customization = customObj,menu_id = menuObj, customUser = request.user, quantity = 1)
				cartMenuCustomObj.save()
				return Response({"status":"customization applied"}) 



