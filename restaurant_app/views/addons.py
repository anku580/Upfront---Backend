
# django imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import QueryDict

# project imports
from restaurant_app.models import Restaurant
from restaurant_app.serializers import RestaurantSerializer
from restaurant_app.views import custom_messages
from myuser.permissions import AdminAllowedPermission,MerchantAllowedPermission

@api_view(['GET'])
@permission_classes([AdminAllowedPermission])
def fetchInactiveRestaurant(request):
    json_response_obj = {}
    all_restaurants = Restaurant.objects.filter(is_activated=False)
    restaurant_serializer = RestaurantSerializer(all_restaurants,many=True)
    json_response_obj['message'] = custom_messages.INACTIVE_RESTAURANT_RETRIEVE_SUCCESS_MSG
    json_response_obj['restaurants'] = restaurant_serializer.data
    return Response(json_response_obj,status = status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AdminAllowedPermission])
def activateRestaurant(request,resid):
    json_response_obj = {}
    restaurant_obj = Restaurant.objects.get(id=resid)
    restaurant_obj.is_activated = True
    restaurant_obj.approved_admin_id = request.user
    restaurant_obj.save()
    restaurant_serializer = RestaurantSerializer(restaurant_obj)
    json_response_obj['message'] = custom_messages.RESTAURANT_ACTIVATION_SUCCESS_MSG
    json_response_obj['restaurant'] = restaurant_serializer.data
    return Response(json_response_obj,status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AdminAllowedPermission|MerchantAllowedPermission,])
def fetchMerchantRestaurants(request):
    json_response_obj = {}
    all_restaurants = Restaurant.objects.filter(res_user=request.user)
    restaurant_serializer = RestaurantSerializer(all_restaurants,many=True)
    json_response_obj['message'] = custom_messages.RESTAURANT_RETRIEVE_SUCCESS_MSG
    json_response_obj['restaurants'] = restaurant_serializer.data
    return Response(json_response_obj,status = status.HTTP_200_OK)

