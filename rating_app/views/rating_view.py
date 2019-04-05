
# django imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# project imports
from rating_app.serializers import RatingSerializer

class RatingView(APIView):

    http_method_names = ['get','post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        json_response_obj = {}
        json_response_obj['message'] = "HTTP " + request.method + " not allowed on this endpoint !"
        return Response(json_response_obj, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, kwargs)

    def post(self, request, kwargs):
        json_response_obj = {}
        request.data['order_id'] = kwargs['order_id']
        rating_serializer = RatingSerializer(data=request.data)
        if rating_serializer.is_valid():
            rating_serializer.save()
            json_response_obj['message'] = "Thank you !"
            json_response_obj['rating'] = rating_serializer.data
            return Response(json_response_obj, status=status.HTTP_201_CREATED)
        else:
            json_response_obj['error'] = rating_serializer.errors
            return Response(json_response_obj, status=status.HTTP_400_BAD_REQUEST)