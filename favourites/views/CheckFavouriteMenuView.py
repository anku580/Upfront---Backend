
from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from menu_app.models import Menu
from favourites.models import FavoriteRestaurant
import base64
from django.contrib.staticfiles.templatetags.staticfiles import static
from menu_app.serializers import MenuSerializer
# Create your views here.

class CheckFavouriteMenuView(APIView):
	def get(self,request,id = None):
		if(id == None):
			return Response({"error":"enter an id"})
		try:
			menuObj =  Menu.objects.get(id = id)
			favMenuObj = FavoriteMenu.objects.get(favMenuUser =request.user.id , favMenu = id )
			return Response({"status":"true"})
		except Menu.DoesNotExist:
			return Response({"error":"a Menu with id = " + str(id) + " does not exist"}, status=status.HTTP_404_NOT_FOUND)
		except FavoriteMenu.DoesNotExist:
			return Response({"status":"false"})