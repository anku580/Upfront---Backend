
# django imports

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json

# project imports
from restaurant_app.models import Restaurant
from restaurant_app.permissions import RestaurantOwnerShipPermission
from restaurant_app.validator import Validator
from restaurant_app.views import custom_messages
from menu_app.models import Category,Menu
from menu_app.serializers import MenuSerializer
from restaurant_app.serializers import RestaurantSerializer
from customization_app.serializers import CustomizationSerializer
from customization_app.models import MenuCustomization, Customization


class MerchantMenuView(APIView,Validator):

    http_method_names = ['get']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        if super().isValidRestaurant(kwargs['resid']) is False:
            return JsonResponse(super().INVALID_RESTAURANT_MSG,status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request,kwargs)

    def get(self,request,kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        all_categories = Category.objects.filter(res_id=kwargs['resid'])
        all_menus_objs = []
        for category in all_categories:
            menu_list_obj = {}
            menu_list = []
            menu_list_obj['category_id'] = category.id
            menu_list_obj['category'] = category.name
            all_menus = Menu.objects.filter(category_id=category)
            for menu in all_menus:
                menu_serializer = MenuSerializer(menu)

                #filtering the customization objects for this menu
                menu_customization_objs = MenuCustomization.objects.filter(menu_id=menu.id).values('customization_id')
                customization_objs = Customization.objects.filter(id__in=menu_customization_objs)

                customization_serializer = CustomizationSerializer(customization_objs, many=True)
                custimization_dict =  {}
                custimization_dict['customizations'] = customization_serializer.data
                custimization_dict.update(menu_serializer.data)
                menu_list.append(custimization_dict)
            menu_list_obj['menus'] = menu_list
            all_menus_objs.append(menu_list_obj)
        json_response_obj['menus'] = all_menus_objs
        json_response_obj['res_id'] = restaurant_obj.id
        json_response_obj['restaurant_name'] = restaurant_obj.name
        json_response_obj['distance'] = "400mts"
        json_response_obj['ratings'] = 4.1
        json_response_obj['no_of_dishes'] = Menu.objects.filter(res_id=kwargs['resid']).count()
        return Response(json_response_obj,status=status.HTTP_200_OK)

