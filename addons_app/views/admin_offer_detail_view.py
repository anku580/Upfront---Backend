
# django imports
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# project imports
from addons_app.models import PromotionOffer
from addons_app import custom_messages
from addons_app.serializers import AdminOfferSerializer
from myuser.permissions import AdminAllowedPermission

class AdminOfferDetailView(APIView):

    permission_classes = (IsAuthenticated,AdminAllowedPermission,)

    http_method_names = ['get','put','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def get(self,request,id):
        json_response_obj = {}
        offer_obj = get_object_or_404(PromotionOffer, id=id)
        offer_serializer = AdminOfferSerializer(offer_obj)
        json_response_obj['message'] = custom_messages.ADMIN_OFFER_RETRIEVED_SUCCESS
        json_response_obj['promotion'] = offer_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)


    def put(self,request,id):
        json_response_obj = {}
        offer_obj = get_object_or_404(PromotionOffer, id=id)
        offer_serializer = AdminOfferSerializer(offer_obj,request.data)
        if offer_serializer.is_valid():
            offer_serializer.save()
            json_response_obj['message'] = custom_messages.ADMIN_OFFER_UPDATED_SUCCESS
            json_response_obj['promotion'] = offer_serializer.data
            return Response(json_response_obj,status = status.HTTP_200_OK)
        else:
            json_response_obj['message'] = offer_serializer.errors
            return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        json_response_obj = {}
        offer_obj = get_object_or_404(PromotionOffer,id=id)
        offer_obj.delete()
        json_response_obj['message'] = custom_messages.ADMIN_OFFER_DELETED_SUCCESS
        return Response(json_response_obj,status = status.HTTP_200_OK)