from django.shortcuts import render
from django.http import HttpResponse
from myuser.serializers import CustomerSerializer
from myuser.models import Customer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from referrals.models import  ReferralModel
from referrals.referral import produce_amount_keys
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
# from Email.models import EmailVerificationModelS

# class CustomerSignupView(APIView):
  

#     def post(self, request,):
     
#         serializer = CustomerSerializer(data=request.data)
        
#         print (request.data['password1'])
#         serializer.validate(request.data)
#         print(serializer)
#         if serializer.is_valid():
#             return HTTPResponse(request.data)



class CustomerRecordView(APIView):
    """
    A class based view for creating and fetching Sstudent records
    """
    permission_classes = (AllowAny,)

    def get(self, format=None, referralString=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
     
        return Response(serializer.data)

    def post(self, request,format=None, referralString =None):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        print(request.data)
        username = request.data['customer']['username']
        userEmail =  request.data['custEmail']
       
        print(username)
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            print(request.data)
            obj1 = User.objects.get(username = username)
            # obj1.is_active =False

            obj1.password = make_password(obj1.password)
            obj1.save()
            try:
                custObj = Customer.objects.get(customer = obj1)
            except Customer.DoesNotExist:
                obj1.delete()
                return Response({"error":"customer details not created"})
                
            # custObj = Customer.objects.get(customer = obj1)
            # custObj.custEmail = ''
            # custObj.save()
            # verificationRef = produce_amount_keys(1)
            # emailObj = EmailVerificationModel(emailUser = obj1, referral = verificationRef, email = custObj.custEmail)
            # print("email problem")
            # emailObj.save()

            # send_mail('UPFRONT Email Verification', 'Hi '+ obj1.username + '\n please click below link to your gmail address:\n\n  http://localhost:8000/email/verification/'+verificationRef+' \n\nwith regards,\nUPFRONT Team', 'postmaster@sandboxf197458928244662817c2ee94f42f8e6.mailgun.org', [userEmail])
            if(referralString):
                try:
                    refUserObj = ReferralModel.objects.get( referral = referralString)
                    refUserObj.score += 1
                    refUserObj .save()
                except ReferralModel.DoesNotExist:
                    print("wrong referral")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
