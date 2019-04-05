
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# project imports
from addons_app import custom_messages
from addons_app.serializers import AdminOfferSerializer
from addons_app.models import PromotionOffer
from myuser.permissions import AdminAllowedPermission

class AdminOfferView(APIView):

    permission_classes = (IsAuthenticated,AdminAllowedPermission,)

    http_method_names = ['get','post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED_MSG
        return Response(json_response_obj,status = status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self,request):
        json_response_obj = {}
        admin_offer_serializer = AdminOfferSerializer(data = request.data)
        if admin_offer_serializer.is_valid():
            admin_offer_serializer.save()
            json_response_obj['message'] = custom_messages.ADMIN_OFFER_CREATED_SUCCESS
            json_response_obj['promotion'] = admin_offer_serializer.data
            return Response(json_response_obj,status = status.HTTP_201_CREATED)
        else:
            json_response_obj['message'] = admin_offer_serializer.errors
            return Response(json_response_obj,status = status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        json_response_obj = {}
        all_offers = PromotionOffer.objects.all()
        admin_offer_serializer = AdminOfferSerializer(all_offers,many = True)
        json_response_obj['message'] = custom_messages.ADMIN_OFFER_RETRIEVED_SUCCESS
        json_response_obj['promotions'] = admin_offer_serializer.data
        return Response(json_response_obj,status = status.HTTP_200_OK)