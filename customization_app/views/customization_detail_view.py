
# project imports
from customization_app import custom_messages
from customization_app.models import Customization
from customization_app.serializers import CustomizationSerializer

# django imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class CustomizationDetailView(APIView):

    http_method_names = ['put','get','delete']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + custom_messages.HTTP_METHOD_NOT_ALLOWED
        return Response(json_response_obj, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,kwargs)

    def get(self,request,kwargs):
        json_response_obj = {}
        customization_obj = Customization.objects.get(id=kwargs['cus_id'])
        customization_serializer = CustomizationSerializer(customization_obj)
        json_response_obj['message'] = custom_messages.CUSTOMIZATION_RETRIEVED_SUCCESS_MSG
        json_response_obj['customization'] = customization_serializer.data
        return Response(json_response_obj, status=status.HTTP_200_OK)

    def put(self,request,kwargs):
        json_response_obj = {}
        request.data['res_id'] = kwargs['resid']
        customization_obj = Customization.objects.get(id=kwargs['cus_id'])
        customization_serializer = CustomizationSerializer(customization_obj, data=request.data)
        if customization_serializer.is_valid():
            customization_serializer.save()
            json_response_obj['message'] = custom_messages.CUSTOMIZATION_UPDATED_SUCCESS_MSG
            json_response_obj['customization'] = customization_serializer.data
            return Response(json_response_obj, status=status.HTTP_200_OK)
        else:
            json_response_obj['message'] = customization_serializer.errors
            return Response(json_response_obj, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,kwargs):
        json_response_obj = {}
        customization_obj = Customization.objects.get(id=kwargs['cus_id'])
        customization_obj.delete()
        json_response_obj['message'] = custom_messages.CUSTOMIZATION_DELETED_SUCCESS_MSG
        return Response(json_response_obj, status=status.HTTP_200_OK)
