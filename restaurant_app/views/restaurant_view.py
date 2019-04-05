# django imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# project imports
from restaurant_app.models import Restaurant
from restaurant_app.serializers import RestaurantSerializer
from restaurant_app.filters import RestaurantFilter
from restaurant_app.views import custom_messages
from restaurant_app.permissions import MerchantViewPermission

class RestaurantView(APIView):

    permission_classes = (IsAuthenticated,MerchantViewPermission)

    http_method_names = ['post','get']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj, status=status.HTTP_200_OK)

    def post(self,request):
        json_response_obj = {}
        request.data['res_user'] = request.user.id
        request.data['is_activated'] = False
        request.data['approved_admin_id'] = None
        restaurant_serializer = RestaurantSerializer(data = request.data)
        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            json_response_obj['message'] = custom_messages.RESTAURANT_CREATED_SUCCESS_MSG
            json_response_obj['restaurant'] = restaurant_serializer.data
            return Response(json_response_obj,status = status.HTTP_201_CREATED)
        json_response_obj['message'] = restaurant_serializer.errors
        return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        json_response_obj = {}
        all_restaurants = Restaurant.objects.filter(is_activated=True)
        rest_filter = RestaurantFilter(request.GET,queryset=all_restaurants)
        restaurant_serializer = RestaurantSerializer(rest_filter.qs,many=True)
        if len(rest_filter.qs) == 0:
            json_response_obj['message'] = custom_messages.NO_RESTAURANT_AVAILABLE_MSG
        else:
            json_response_obj['message'] = custom_messages.RESTAURANT_RETRIEVE_SUCCESS_MSG
        json_response_obj['restaurants'] = restaurant_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)
