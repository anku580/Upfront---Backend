
# project imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict

# django imports
from restaurant_app.views import custom_messages
from restaurant_app.filters import RestaurantFilter
from restaurant_app.models import Restaurant
from restaurant_app.serializers import RestaurantSerializer


class NearbyRestaurantView(APIView):

    http_method_names = ['post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self,request):
        json_response_obj = {}
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        params = {"latitude":latitude,"longitude":longitude}
        query_dict = QueryDict('',mutable=True)
        query_dict.update(params)
        query_dict.update(request.query_params)
        all_restaurants = Restaurant.objects.filter(is_activated=True)
        restaurant_filter = RestaurantFilter(query_dict,all_restaurants)
        restaurant_serializer = RestaurantSerializer(restaurant_filter.qs,many=True)
        json_response_obj['message'] = custom_messages.RESTAURANT_RETRIEVE_SUCCESS_MSG
        json_response_obj['restaurants'] = restaurant_serializer.data
        return Response(json_response_obj,status=status.HTTP_200_OK)


