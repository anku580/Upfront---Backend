# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# project imports
from addons_app.serializers import RestaurantOfferSerializer
from addons_app import custom_messages
from restaurant_app.models import Restaurant
from addons_app.models import RestaurantOffer
from restaurant_app.permissions import RestaurantOwnerShipPermission
from restaurant_app.validator import Validator


class RestaurantOfferView(APIView,Validator):

    permission_classes = (IsAuthenticated,RestaurantOwnerShipPermission,)

    http_method_names = ['post','get','put','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        if super().isValidRestaurant(kwargs['resid']) is False:
            return JsonResponse(super().INVALID_RESTAURANT_MSG,status=status.HTTP_400_BAD_REQUEST)
        return super().dispatch(request,kwargs)

    def post(self,request,kwargs):
        json_response_obj = {}
        request.data['res_id'] = kwargs['resid']
        restaurant_offer_serializer = RestaurantOfferSerializer(data = request.data)
        if restaurant_offer_serializer.is_valid():
            restaurant_offer_serializer.save()
            json_response_obj['message'] = custom_messages.RESTAURANT_OFFER_ADDED_SUCCESS_MSG
            json_response_obj['offer'] = restaurant_offer_serializer.data
            return Response(json_response_obj,status = status.HTTP_201_CREATED)
        else:
            json_response_obj['message'] = restaurant_offer_serializer.errors
            return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)

    def get(self,request,kwargs):
        json_response_obj = {}
        offer_obj = RestaurantOffer.objects.filter(res_id=kwargs['resid'])
        restaurant_offer_serializer = RestaurantOfferSerializer(offer_obj,many=True)
        json_response_obj['message'] = custom_messages.RESTAURANT_OFFERS_RETRIEVED_SUCCESS_MSG
        json_response_obj['offer'] = restaurant_offer_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)


