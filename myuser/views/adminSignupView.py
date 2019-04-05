from django.shortcuts import render

from django.http import HttpResponse
from myuser.serializers import UserSerializer
from myuser.models import ConfirmAdmin
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()



class adminSignupView(APIView):
    """
    A class based view for signing up admins
    """
    permission_classes = (AllowAny,)

    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
00         :return: Returns a list of student records
        """
        adminUserObj = User.objects.filter(is_admin =True)
        serializer = UserSerializer(adminUserObj, many=True)
     
        return Response(serializer.data)

    def post(self, request,format=None):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        print(request.data)
        username = request.data['username']
        print(username)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            print(request.data)
            obj1 = User.objects.get(username = username)

            obj1.password = make_password(obj1.password)
           
            obj1.save()
            confirmObj = ConfirmAdmin(admin = obj1)
            confirmObj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
