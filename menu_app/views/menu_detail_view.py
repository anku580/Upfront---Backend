
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# project imports
from menu_app.views import custom_messages
from menu_app.serializers import MenuSerializer,MenuOfferSerializer
from menu_app.models import Menu,Category
from restaurant_app.models import Restaurant
from restaurant_app.validator import Validator
from restaurant_app.permissions import RestaurantOwnerShipPermission
from customization_app.models import Customization, MenuCustomization
from customization_app.serializers import CustomizationSerializer

class MenuDetailView(APIView,Validator):


    http_method_names = ['put','delete','get']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        if super().isValidRestaurant(kwargs['resid']) is False:
            return JsonResponse(super().INVALID_RESTAURANT_MSG,status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request,kwargs)

    def get(self,request,kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        menu_obj = Menu.objects.get(id=kwargs['menuid'])
        menu_serializer = MenuOfferSerializer(menu_obj)
        menu_customization_objs = MenuCustomization.objects.filter(menu_id__id=kwargs['menuid']).values('customization_id')
        customization_objs = Customization.objects.filter(id__in=menu_customization_objs)
        customization_serializer = CustomizationSerializer(customization_objs, many=True)
        customization_dict = {}
        customization_dict['customizations'] = customization_serializer.data
        print(customization_dict)
        customization_dict.update(menu_serializer.data)
        json_response_obj['message'] = custom_messages.MENU_RETRIEVED_SUCCESS_MSG
        json_response_obj['menu'] = customization_dict
        return Response(json_response_obj,status=status.HTTP_200_OK)

    def put(self,request,kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        menu_obj = Menu.objects.get(id=kwargs['menuid'])
        request.data['res_id'] = kwargs['resid']
        request.data['discounted_price'] = request.data['original_price']
        menu_serializer = MenuSerializer(menu_obj,request.data)
        if menu_serializer.is_valid():
            menu_serializer.save()
            json_response_obj['message'] = custom_messages.MENU_UPDATED_SUCCESS_MSG
            json_response_obj['menu'] = menu_serializer.data
            return Response(json_response_obj,status = status.HTTP_200_OK)
        else:
            json_response_obj['message'] = menu_serializer.errors
            return Response(json_response_obj, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        self.check_object_permissions(request, restaurant_obj)
        menu_obj = Menu.objects.get(id=kwargs['menuid'])
        menu_obj.delete()
        json_response_obj['message'] = custom_messages.MENU_DELETED_SUCCESS_MSG
        return Response(json_response_obj, status=status.HTTP_200_OK)
