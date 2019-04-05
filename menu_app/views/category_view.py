# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# project imports
from menu_app.views import custom_messages as custom_message
from menu_app.serializers import CategorySerializer
from menu_app.models import Category
from menu_app.filters import CategoryFilter
from restaurant_app.validator import Validator
from restaurant_app.permissions import RestaurantOwnerShipPermission
from restaurant_app.models import Restaurant

class CategoryView(APIView,Validator):

    http_method_names = ['post','get']

    permission_classes = (RestaurantOwnerShipPermission,)

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_message.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        if super().isValidRestaurant(kwargs['resid']) is False:
            return JsonResponse(super().INVALID_RESTAURANT_MSG,status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request,kwargs)

    def post(self,request,kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        self.check_object_permissions(request,restaurant_obj)
        request.data['res_id'] = kwargs['resid']
        category_serializer = CategorySerializer(data = request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            json_response_obj['message'] = custom_message.CREATED_CATEGORY_SUCCESS_MSG
            json_response_obj['category'] = category_serializer.data
            return Response(json_response_obj,status = status.HTTP_201_CREATED)
        else:
            json_response_obj['message'] = category_serializer.errors
            return Response(json_response_obj,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        self.check_object_permissions(request, restaurant_obj)
        category_objects = Category.objects.filter(res_id=kwargs['resid'])
        category_filter = CategoryFilter(request.GET, category_objects)
        category_serializer = CategorySerializer(category_filter.qs, many=True)
        if len(category_filter.qs) == 0:
            json_response_obj['message'] = custom_message.NO_CATEGORIES_FOUND_MSG
            json_response_obj['categories'] = category_serializer.data
            return Response(json_response_obj,status = status.HTTP_200_OK)
        json_response_obj['message'] = custom_message.CATEGORY_RETRIEVED_SUCCESS_MSG
        json_response_obj['categories'] = category_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)


