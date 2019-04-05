
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from restaurant_app.models import Restaurant
from favourites.models import FavoriteRestaurant
import base64
from django.contrib.staticfiles.templatetags.staticfiles import static
from restaurant_app.serializers import RestaurantSerializer
# Create your views here.

class CheckFavouriteRestaurantView(APIView):
	def get(self,request,id = None):
		if(id == None):
			return Response({"error":"enter an id"})
		try:
			resObj =  Restaurant.objects.get(id = id)
			favResObj = FavoriteRestaurant.objects.get(favResUser =request.user.id , favRes = id )
			return Response({"status":"true"})
		except Restaurant.DoesNotExist:
			return Response({"error":"a Restaurant with id = " + str(id) + " does not exist"}, status=status.HTTP_404_NOT_FOUND)
		except FavoriteRestaurant.DoesNotExist:
			return Response({"status":"false"})