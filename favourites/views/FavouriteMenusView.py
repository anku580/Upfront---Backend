from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from menu_app.models import Menu
from favourites.models import FavoriteMenu
import base64
from django.contrib.staticfiles.templatetags.staticfiles import static
from menu_app.serializers import MenuSerializer
# Create your views here.

class FavouriteMenusView(APIView):
	def post(self, request, id = None):
		responseDict = {}
		try:
			menuObj = Menu.objects.get(id = request.data['menuId'])
		except Menu.DoesNotExist:
			responseDict["error"] = "Menu with  id = " + str( request.data['menuId']) + " not found."
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)  		
		try:	
			favMenuObj = FavoriteMenu.objects.get(favMenu = request.data['menuId'])
			responseDict["error"] = "Menu with  id = " + str( request.data['menuId']) + " already exists in the favourites."
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)
		except FavoriteMenu.DoesNotExist:
				
			menuObj = Menu.objects.get(id = request.data['menuId'])
			favMenuObj = FavoriteMenu(	favMenuUser = request.user, favMenu = menuObj )
			favMenuObj.save()
			responseDict['Menu ' + str(menuObj.id)] = "Menu is added to favourites"
			return Response(responseDict)
	def get (self, request, id = None):

		responseDict = {}
		ids = []
		try:
			favResObj = FavoriteMenu.objects.filter(favMenuUser = request.user)
			for i in favResObj:
				ids.append(i.favMennu.id)
				# resObj = Restaurant.objects.filter(id = i.favRes.id)
				# print('hello1')
				# resObjSerializer = RestaurantSerializer(resObj,many=True)
				# for i in resObjSerializer.data.keys()

				# responseDict[i.favRes.id] = resObjSerializer.data
				# print(type(resObjSerializer.data))
				# print('hello2')

				# print(str(i.favRes.photo))
				# url1 = static(str(i.favRes.photo))
				# str1 = ''
				# with open(i.favRes.photo.path, "rb") as imageFile:
				# 	str1 = base64.b64encode(imageFile.read())
				# print(str1)
				# responseDict[i.favRes.id]["photo"] = str1
				# responseDict[i.favRes.id]["latitude"] = i.favRes.latitude
				# responseDict[i.favRes.id]["longitude"] = i.favRes.longitude
				# responseDict[i.favRes.id]["area"] = i.favRes.area
				# responseDict[i.favRes.id]["city"] = i.favRes.city
				# responseDict[i.favRes.id]["isVeg"] = i.favRes.is_veg



    		
			menubj = Menu.objects.filter(id__in = ids)
			menuObjSerializer = RestaurantSerializer(menuObj,many=True)
			return Response(menuObjSerializer.data) 
			
		except FavoriteMenu.DoesNotExist:
			responseDict["error"] = "you have not added Menus to favourites"

	def delete(self, request, id = None):
		responseDict = {}
		try:
			menuObj = Menu.objects.get(id = id)
		except Menu.DoesNotExist:
			responseDict["error"] = "menu with  id = " + str( id) + " not found."
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)  		
		try:	
			favMenuObj = FavoriteMenu.objects.get(favMenu = id)
			menuObj = Menu.objects.get(id = id)	
			favMenuObj = FavoriteMenu.objects.get(	favMenuUser = request.user, favMenu = menuObj.id )
			favMenuObj.delete()
			responseDict['menu ' + str(menuObj.id)] = "menu is removed from favourites"
			return Response(responseDict)
		except FavoriteMenu.DoesNotExist:
				
			responseDict["error"] = "menu with  id = " + str( id) + " does not exists in the favourites."
		
			
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)