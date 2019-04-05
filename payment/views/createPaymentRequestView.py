from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from django.http import HttpResponse
from django.views.generic import View 
from rest_framework.permissions import AllowAny
from temperorycart.models import Cart, PermanentCart, TotalCost , Order, BillModel
from myuser.models import Merchant
from temperorycart.serializers import CartSerializer, QuantityIncrementSerializer,OrderSerializer
from payment import Checksum
import requests
import base64
import json

class CreatePaymentRequestView(APIView):
	permission_classes = (AllowAny,)

	def post(self,request):
		bills ={}
		MERCHANT_KEY = '2uE5Gn#pU5hcXdJ8'.encode()
		
		orderObj = Order.objects.get(orderNo = request.data['orderNo'])
		# for i in obj1.orderRestaurants.all():
		order_id  = str(224 + orderObj.orderNo.id)
		
		# 	obj2 = BillModel.objects.get(orderNo = request.data['orderNo'],billResId = i.id)
		# 	print('hello:',i.res_user)
		# 	MerchObj = Merchant.objects.get(merchant= i.res_user)				
		# 	print(MerchObj)


			
		# 	print (obj1.orderNo.Totalcost)
		data_dict = {
				'MID':'HYqgIk22213857160559',
				'ORDER_ID':order_id,
				'TXN_AMOUNT':str(orderObj.totalcost)+'.00',
				'CUST_ID':request.user.username,
				'INDUSTRY_TYPE_ID':'Retail',
				'WEBSITE':'WEBSTAGING',
				'CHANNEL_ID':'WEB',
				'CALLBACK_URL':'http://127.0.0.1:8000/orders/response/',
		}


		param_dict = data_dict  

		param_dict['CHECKSUMHASH'] =Checksum.generate_checksum(data_dict, MERCHANT_KEY)

		bills['bill'] = param_dict

		if 'bill' in bills.keys():
			return Response( bills )
		else:
			return Response({'status':'failure'})
