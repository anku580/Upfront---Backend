
# project imports
from customization_app import custom_messages
from customization_app.models import Customization
from customization_app.serializers import CustomizationSerializer

# django imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class CustomizationView(APIView):

    http_method_names = ['post','get']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method +custom_messages.HTTP_METHOD_NOT_ALLOWED
        return Response(json_response_obj,status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,kwargs)

    def post(self,request,kwargs):
        json_resonse_obj = {}
        request.data['res_id'] = kwargs['resid']
        customization_serializer = CustomizationSerializer(data=request.data)
        if customization_serializer.is_valid():
            customization_serializer.save()
            json_resonse_obj['message'] = custom_messages.CUSTOMIZATION_ADDED_SUCCESS_MSG
            json_resonse_obj['customization'] = customization_serializer.data
            return Response(json_resonse_obj, status=status.HTTP_201_CREATED)
        else:
            json_resonse_obj['message'] = customization_serializer.errors
            return Response(json_resonse_obj, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,kwargs):
        json_response_obj = {}
        all_customizations = Customization.objects.filter(res_id=kwargs['resid'])
        customization_serializer = CustomizationSerializer(all_customizations,many=True)
        print(customization_serializer.data)
        json_response_obj['message'] = custom_messages.CUSTOMIZATION_RETRIEVED_SUCCESS_MSG
        json_response_obj['customizations'] = customization_serializer.data
        return Response(json_response_obj, status=status.HTTP_200_OK)