# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

# project imports
from menu_app.views import custom_messages
from menu_app.models import Category
from menu_app.serializers import CategorySerializer
from restaurant_app.models import Restaurant
from restaurant_app.permissions import RestaurantOwnerShipPermission
from menu_app.permissions import CategoryOwnershipPermission
from restaurant_app.validator import Validator

class CategoryDetailView(APIView,Validator):

    permission_classes = (CategoryOwnershipPermission,)

    http_method_names = ['get','put','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        if super().isValidRestaurant(kwargs['resid']) is False:
            return JsonResponse(super().INVALID_RESTAURANT_MSG,status=status.HTTP_400_BAD_REQUEST)
        elif super().isValidCategory(kwargs['categoryid']) is False:
            return JsonResponse(super().INVALID_CATEGORY_MSG,status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request,kwargs)

    def delete(self,request,kwargs):
        json_response_obj = {}
        category_obj = Category.objects.get(id=kwargs['categoryid'])
        self.check_object_permissions(request, category_obj)
        category_obj.delete()
        json_response_obj['message'] = custom_messages.CATEGORY_DELETED_SUCCESS_MSG
        return Response(json_response_obj,status = status.HTTP_200_OK)

    def get(self,request,kwargs):
        json_response_obj = {}
        category_obj = Category.objects.get(id=kwargs['categoryid'])
        self.check_object_permissions(request, category_obj)
        category_serializer = CategorySerializer(category_obj)
        json_response_obj['message'] = custom_messages.CATEGORY_RETRIEVED_SUCCESS_MSG
        json_response_obj['category'] = category_serializer.data
        return Response(json_response_obj, status=status.HTTP_200_OK)

    def put(self,request,kwargs):
        json_response_obj = {}
        category_obj = Category.objects.get(id=kwargs['categoryid'])
        self.check_object_permissions(request, category_obj)
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        request.data['res_id'] = restaurant_obj.id
        category_serializer = CategorySerializer(category_obj,data = request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            json_response_obj['message'] = custom_messages.CATEGORY_UPDATE_SUCCESS_MSG
            json_response_obj['category'] = category_serializer.data
            return Response(json_response_obj,status = status.HTTP_200_OK)
        else:
            json_response_obj['message'] = category_serializer.errors
            return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)



