
from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.views.generic import View 
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator
from payment import Checksum
from temperorycart.models import Order
import datetime
import pytz
import base64
import json

import cgi

class OrderResponseView(APIView):

	permission_classes = (AllowAny,)
	
	# def get(self,request):

	# 	print('checking paytm response:',request.data['RESPCODE'],request.data.keys())
	# 	MERCHANT_KEY = '2uE5Gn#pU5hcXdJ8';


	# 	form = request.data
	# 	respons_dict = {}

	# 	for i in form.keys():
	# 		respons_dict[i]=form[i].value
	# 		if i=='CHECKSUMHASH':
	# 			checksum = form[i].value

	# 	if 'GATEWAYNAME' in respons_dict:
	# 		if respons_dict['GATEWAYNAME'] == 'WALLET':
	# 			respons_dict['BANKNAME'] = 'null';

	# 	verify = Checksum.verify_checksum(respons_dict, MERCHANT_KEY, checksum)
	# 	print (verify)

	# 	if verify:
	# 		if respons_dict['RESPCODE'] == '01':
	# 			print("order successful")
	# 		else:
	# 			print("order unsuccessful because"+respons_dict['RESPMSG'])
	# 	else: 
	# 		print("order unsuccessful because"+respons_dict['RESPMSG'])

	# 	return Response(request.data)


	def post(self,request):

		# print('post request.data:',request.data)

		print('checking paytm response:',request.data['RESPCODE'],request.data.keys())
		MERCHANT_KEY = '2uE5Gn#pU5hcXdJ8';
		orderStatusMessage = None
		verify = False

		form = request.data
		respons_dict = {}

		for i in form.keys():
			respons_dict[i]=form[i]
			if i=='CHECKSUMHASH':
				checksum = form[i]
				
				verify = Checksum.verify_checksum(respons_dict, MERCHANT_KEY.encode(), checksum)
				print (verify)

		if 'GATEWAYNAME' in respons_dict:
			if respons_dict['GATEWAYNAME'] == 'WALLET':
				respons_dict['BANKNAME'] = 'null';

		

		if verify:
			if respons_dict['RESPCODE'] == '01':
				orderStatusMessage = "order successful"
				print('orderID :',respons_dict['ORDERID'],type(respons_dict['ORDERID']))
				orderObj = Order.objects.get(orderNo = (int(respons_dict['ORDERID'])-224))
				tz = pytz.timezone('GMT')
				currentDT = datetime.datetime.now(tz)
				currentDT  = currentDT + datetime.timedelta(hours=5,minutes = 30) 
				orderObj.paymentCompleted =True
				orderObj.orderPaidTime = currentDT
				orderObj.save()
			else:
				orderStatusMessage = "order unsuccessful because "+respons_dict['RESPMSG']
		else: 
			orderStatusMessage = "order unsuccessful because "+respons_dict['RESPMSG']
		orderStatus = { 'order status':orderStatusMessage}
		return Response(orderStatus)
