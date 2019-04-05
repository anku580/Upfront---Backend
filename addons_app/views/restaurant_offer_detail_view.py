
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# project imports
from addons_app.serializers import RestaurantOfferSerializer
from addons_app import custom_messages
from addons_app.models import RestaurantOffer
from menu_app.models import Menu
from addons_app.views.addons import applyOfferToMenu,removeOfferFromMenu

class RestaurantOfferDetailView(APIView):


    http_method_names = ['get','put','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def get(self,request,resid,offerid):
        json_response_obj = {}
        offer_obj = RestaurantOffer.objects.get(id=offerid)
        restaurant_offer_serializer = RestaurantOfferSerializer(offer_obj)
        json_response_obj['message'] = custom_messages.RESTAURANT_OFFERS_RETRIEVED_SUCCESS_MSG
        json_response_obj['offer'] = restaurant_offer_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)

    def put(self,request,resid,offerid):
        json_response_obj = {}
        offer_obj = RestaurantOffer.objects.get(id=offerid)
        request.data['res_id'] = resid
        restaurant_offer_serializer = RestaurantOfferSerializer(offer_obj,data = request.data)
        if restaurant_offer_serializer.is_valid():
            restaurant_offer_serializer.save()
            for menu in Menu.objects.filter(offer_id=offerid):
                applyOfferToMenu(menu.id,offerid)
            json_response_obj['message'] = custom_messages.RESTAURANT_OFFER_UPDATED_SUCCESS_MSG
            json_response_obj['offer'] = restaurant_offer_serializer.data
            return Response(json_response_obj,status = status.HTTP_200_OK)
        else:
            json_response_obj['message'] = restaurant_offer_serializer.errors
            return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)


    def delete(self,request,resid,offerid):
        json_response_obj = {}
        for menu in Menu.objects.filter(offer_id=offerid):
            removeOfferFromMenu(menu.id)
        offer_obj = RestaurantOffer.objects.get(id=offerid)
        offer_obj.delete()
        json_response_obj['message'] = custom_messages.RESTAURANT_OFFER_DELETED_SUCCESS_MSG
        return Response(json_response_obj,status = status.HTTP_200_OK)
