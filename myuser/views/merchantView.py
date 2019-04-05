from django.shortcuts import render

from django.http import HttpResponse
from myuser.serializers import MerchantSerializer
from myuser.models import Merchant

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
User = get_user_model()
from myuser.models import Merchant
from django.contrib.auth.hashers import make_password
from referrals.models import  ReferralModel

# Create your views here.





from rest_framework.permissions import AllowAny


class MerchantRecordView(APIView):
    """
    A class based view for creating and fetching student records
    """
    permission_classes = (AllowAny,)
    def get(self, format=None, referralString =None):

        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        merchant = Merchant.objects.all()
        serializer = MerchantSerializer(merchant, many=True)
        
        return Response(serializer.data)

    def post(self, request,format=None, referralString =None):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        serializer = MerchantSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            username = request.data['merchant']['username']
            print(username)
            serializer.create(validated_data=request.data)
            obj1 = User.objects.get(username = username)
            obj1 .is_merchant = True
            obj1.is_active =True
            obj1.password = make_password(obj1.password)
            obj1.save()
            try:
                merchObj = Merchant.objects.get(merchant = obj1)
            except Merchant.DoesNotExist:
                obj1.delete()
                return Response({"error":"merchant details not created"})
            if(referralString):
                try:
                    refUserObj = ReferralModel.objects.get( referral = referralString)
                    refUserObj.score += 2  
                    refUserObj .save()
                except ReferralModel.DoesNotExist:
                    print("wrong referral")
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
 