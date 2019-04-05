from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from restaurant_app.models import Restaurant
from favourites.models import FavoriteRestaurant
import base64
from django.contrib.staticfiles.templatetags.staticfiles import static
from restaurant_app.serializers import RestaurantSerializer
# Create your views here.

class FavouriteRestaurantsView(APIView):
	def post(self, request, id = None):
		responseDict = {}
		try:
			resObj = Restaurant.objects.get(id = request.data['resId'])
		except Restaurant.DoesNotExist:
			responseDict["error"] = "restaurant with  id = " + str( request.data['resId']) + " not found."
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)  		
		try:	
			favResObj = FavoriteRestaurant.objects.get(favRes = request.data['resId'])
			responseDict["error"] = "restaurant with  id = " + str( request.data['resId']) + " already exists in the favourites."
			return Response(responseDict, status=status.HTTP_400_BAD_REQUEST)
		except FavoriteRestaurant.DoesNotExist:
				
			resObj = Restaurant.objects.get(id = request.data['resId'])
			favResObj = FavoriteRestaurant(	favResUser = request.user, favRes = resObj )
			favResObj.save()
			responseDict['restaurant ' + str(resObj.id)] = "restaurant is added to favourites"
			return Response(responseDict)
	def get (self, request, id = None):

		responseDict = {}
		ids = []
		try:
			favResObj = FavoriteRestaurant.objects.filter(favResUser = request.user)
			for i in favResObj:
				ids.append(i.favRes.id)
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



    		
			resObj = Restaurant.objects.filter(id__in = ids)
			resObjSerializer = RestaurantSerializer(resObj,many=True)
			return Response(resObjSerializer.data) 
			
		except FavoriteRestaurant.DoesNotExist:
			responseDict["error"] = "you have not added any restaurants to favourites"

	def delete(self, request, id = None):
		if (id == None):
			return({"error":"id not mentiontioned"})
		responseDict = {}
		try:
			resObj = Restaurant.objects.get(id = id)
		except Restaurant.DoesNotExist:
			responseDict["error"] = "restaurant with  id = " + str( id) + " not found."
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)  		
		try:	
			favResObj = FavoriteRestaurant.objects.get(favRes =id)
			resObj = Restaurant.objects.get(id = id)	
			favResObj = FavoriteRestaurant.objects.get(	favResUser = request.user, favRes = resObj.id )
			favResObj.delete()
			responseDict['restaurant ' + str(resObj.id)] = "restaurant is removed from favourites"
			return Response(responseDict)
		except FavoriteRestaurant.DoesNotExist:
				
			responseDict["error"] = "restaurant with  id = " + str( id) + " does not exists in the favourites."
		
			
			return Response(responseDict, status=status.HTTP_400_BAD_REQUES)