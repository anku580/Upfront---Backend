# django imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
# project imports
from restaurant_app.models import Restaurant
from restaurant_app.serializers import RestaurantSerializer
from restaurant_app.views import custom_messages
from restaurant_app.validator import Validator
from restaurant_app.permissions import RestaurantOwnerShipPermission


class RestaurantDetailView(APIView,Validator):

    permission_classes = (IsAuthenticated,RestaurantOwnerShipPermission)

    http_method_names = ['get','put','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP "+request.method + custom_messages.METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        if super().isValidRestaurant(kwargs['resid']) is False:
            return JsonResponse(super().INVALID_RESTAURANT_MSG,status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request,kwargs)

    def get(self, request, kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        self.check_object_permissions(request, restaurant_obj)
        restaurant_serializer = RestaurantSerializer(restaurant_obj)
        json_response_obj['message'] = custom_messages.RESTAURANT_RETRIEVE_SUCCESS_MSG
        json_response_obj['restaurants'] = restaurant_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)

    def delete(self, request, kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        self.check_object_permissions(request, restaurant_obj)
        restaurant_obj.delete()
        json_response_obj['message'] = custom_messages.RESTAURANT_DELETE_SUCCESS_MSG
        return Response(json_response_obj, status = status.HTTP_200_OK)

    def put(self, request, kwargs):
        json_response_obj = {}
        restaurant_obj = Restaurant.objects.get(id=kwargs['resid'])
        self.check_object_permissions(request, restaurant_obj)
        request.data['res_user'] = request.user.id
        restaurant_serializer = RestaurantSerializer(restaurant_obj , data = request.data)
        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            json_response_obj['message'] = custom_messages.RESTAURANT_UPDATE_SUCCESS_MSG
            json_response_obj['restaurant'] = restaurant_serializer.data
            return Response(json_response_obj,status = status.HTTP_200_OK)
        json_response_obj['message'] = restaurant_serializer.errors
        return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)

