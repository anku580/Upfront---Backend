# project imports
from customization_app import custom_messages
from customization_app.models import Customization, MenuCustomization
from menu_app.models import Menu
from customization_app.serializers import CustomizationSerializer, MenuCustomSerializer

# django imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class MenuCustomizationView(APIView):

    http_method_names = ['put','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " +request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED
        return Response(json_response_obj, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,kwargs)

    def put(self,request,kwargs):
        json_response_obj = {}
        if MenuCustomization.objects.filter(menu_id=kwargs['menu_id'], customization_id=kwargs['cus_id']).count() == 1:
            json_response_obj['message'] = custom_messages.CUSTOMIZATION_ALREADY_APPLIED_TO_MENU
            return Response(json_response_obj, status=status.HTTP_200_OK)
        request.data['menu_id'] = kwargs['menu_id']
        request.data['customization_id'] = kwargs['cus_id']
        menu_custom_serializer = MenuCustomSerializer(data=request.data)
        if menu_custom_serializer.is_valid():
            menu_custom_serializer.save()
            json_response_obj['message'] = custom_messages.CUSTOMIZATION_APPLIED_TO_MENU
            return Response(json_response_obj, status=status.HTTP_200_OK)
        else:
            json_response_obj["message"] = menu_custom_serializer.errors
            return Response(json_response_obj, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,kwargs):
        json_response_obj = {}
        if MenuCustomization.objects.filter(menu_id=kwargs['menu_id'], customization_id=kwargs['cus_id']).count() == 0:
            json_response_obj['message'] = custom_messages.CUSTOMIZATION_NOT_APPLIED_MENU
            return Response(json_response_obj, status=status.HTTP_200_OK)
        menu_customization = MenuCustomization.objects.get(menu_id=kwargs['menu_id'], customization_id=kwargs['cus_id'])
        menu_customization.delete()
        json_response_obj['message'] = custom_messages.CUSTOMIZATION_REMOVED_FROM_MENU
        return Response(json_response_obj, status=status.HTTP_200_OK)