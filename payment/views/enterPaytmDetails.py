from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
# from temperoryCart.models import Cart, PermanentCart, TotalCost , Order, BillModel
# from myUser.models import Merchant
from payment.models import PaytmDetails
from temperorycart.serializers import CartSerializer, QuantityIncrementSerializer,OrderSerializer
from payment import Checksum
import requests
import base64
import json

class enterPaytmDetails(APIView):
	def get(self,request):
		details = {}
		try :
			paytmObj = PaytmDetails.objects.get(PaytmUser = request.user)
			details ['user'] = request.user.username
			details['paytmId'] = paytmObj.PaytmId
			details['paytmKey'] = paytmObj.PaytmKey
		except PaytmDetails.DoesNotExist:
			details['error'] = 'you have entered your paytm details'

		return Response(details)
	def post(self,request):

		paytmObj = PaytmDetails(	PaytmUser = request.user,PaytmId = request.data['paytmId'] ,PaytmKey = request.data['paytmKey'] )
		paytmObj.save()
		obj = PaytmDetails.objects.get(PaytmUser = request.user.id)
		status= {}
		if (obj):
			status = {'status': 'record created successfully'}
		else:
			status = {'status': 'record not created'}

		return Response(status)
	def put(self,request):

		paytmObj = PaytmDetails.objects.get(PaytmUser = request.user)
		status = {}
		status['paytmKey'] = 'paytmKey has not been changed'
		status['paytmId'] = 'paytmId has not been changed'

		if 'paytmId' in  request.data .keys():
			paytmObj.PaytmId = request.data['paytmId']
			status['paytmId'] = 'paytmId has been changed'
		if 'paytmKey' in  request.data .keys():
			paytmObj.PaytmKey = request.data['paytmKey']
			status['paytmKey'] = 'paytmKey has been changed'

		paytmObj.save()
		
		

		return Response(status)