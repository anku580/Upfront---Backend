from django.shortcuts import render

from django.http import HttpResponse
from myuser.serializers import SubAdminSerializer
from myuser.models import SubAdmin,Merchant
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()

# class CustomerSignupView(APIView):
  

#     def post(self, request,):
     
#         serializer = CustomerSerializer(data=request.data)
        
#         print (request.data['password1'])
#         serializer.validate(request.data)
#         print(serializer)
#         if serializer.is_valid():
#             return HTTPResponse(request.data)




class SubAdminRecordView(APIView):
    """
    A class based view for creating and fetching student records
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        merchObj  =  Merchant.objects.get(merchant = request.user.id)
        subObj = SubAdmin.objects.filter(merchant =  merchObj.merchantId)
        print(subObj)
        serializer = SubAdminSerializer(subObj, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request,format=None):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        # print(request.data)
        obj2 = Merchant.objects.get(merchant=request.user.id)
      
       
        request.data['merchant'] = obj2.merchantId
      
        username = request.data['subuser']['username']
        print(username)
        serializer = SubAdminSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            print(request.data)
            obj1 = User.objects.get(username = username)
            obj1.is_subadmin = True
            obj1.is_merchant = True
            obj1.password = make_password(obj1.password)
            obj1.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
