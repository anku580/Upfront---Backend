

from myuser.serializers import   LoginCustomerSerializer

from myuser.renderers import UserJSONRenderer
from rest_framework.permissions import AllowAny


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginCustomerAPIView(APIView):
    permission_classes = (AllowAny,)

    
    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        context = {
        'message': 'enter your username and password for logging in'
        }
        return Response(context)

    def post(self, request,format=None):
      
        print(request.data['password'])
        data1 = {}
        serializer = LoginCustomerSerializer(data=request.data)
        
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
    
       
        if serializer.is_valid(raise_exception=True,):
            data1 = serializer.validate1(data=request.data)
      
        print('serializer.data:',serializer.data)

        return Response(data1, status=status.HTTP_200_OK)

