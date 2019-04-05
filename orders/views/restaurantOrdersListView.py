from rest_framework import status
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from temperorycart.models import Order, Cart, PermanentCart
from menu_app.models import Menu
from orders.serializers import OrderRestaurantSerializer
from temperorycart.serializers import PermanentCartSerializer

class restaurantOrdersListView(APIView):
	def get(self,request, resId = None):
		orderObj = Order.objects.filter(Status = 1 )
		serializer  = OrderRestaurantSerializer(orderObj,many = True)
		restaurantOrderDict = {}
		tempDict = {}

		for i in serializer.data:
			for j in i:
				if j == 'orderNo':
					print('orderNo',i[j])
					PermanentCartObj = PermanentCart.objects.filter(orderNo = i[j])
					orderObj =Order.objects.filter(orderNo = i[j])
					# for i in range(len(PermanentCartObj)):
					# 	print('checking123',PermanentCartObj['date_created'])
					# # print('length:',len(PermanentCartObj))
					# tempDict [i[j]] = {}
					for i in range(len(PermanentCartObj)):
						flag = True
						
						print('length',PermanentCartObj[i].date_created.strftime("%I:%M:%S %p"))
						if  PermanentCartObj[i].cartItem.res_id.id not in restaurantOrderDict.keys():
							restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id]  = {}

						if  PermanentCartObj[i].orderNo.id not in  restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id].keys():
							restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id] = {}
							restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['items'] = {}

						restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['restaurantConfirmation'] = PermanentCartObj[i].restaurantConfirmation

						# print('check error occured before here',PermanentCartObj[i].cartItem.res_id.id)

						# while flag == True:
						# tempDict[PermanentCartObj[i].orderNo.id][PermanentCartObj[i].cartItem.name] = PermanentCartObj[i].quantity
						
						restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['items'][PermanentCartObj[i].cartItem.name] =PermanentCartObj[i].quantity
							# if(PermanentCartObj[i].cartItem.name in restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id].keys()):
								# print(restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id].keys())
			

						restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['order_created'] =PermanentCartObj[i].date_created.strftime("%I:%M:%S %p")
				# print('----- --------- ------- - - - -- -- - --- ---- -- -')

		print(restaurantOrderDict)
		print(tempDict)
		if resId == None:
			return Response(restaurantOrderDict)
		else:
			return Response(restaurantOrderDict[resId])
	def post( self,request ):
		acceptedOrderNoList = request.data['acceptedOrderNoList']
		status =  {}
		print(request.user)
		if acceptedOrderNoList == None :
			status['acceptedOrderStatus'] =  'no Orders are rejected'
		
		else:
		
			for i in acceptedOrderNoList:
				flag = 1 
				orderObj = Order.objects.get(orderNo = i)
				PermanentCartObj = PermanentCart.objects.filter(orderNo = i)

				for i in range(len(PermanentCartObj)):
					if PermanentCartObj[i].cartItem.res_id.res_user == request.user:

						print(PermanentCartObj[i].cartItem.res_id.name)
						PermanentCartObj[i].restaurantConfirmation = True
						PermanentCartObj[i].save()
					if PermanentCartObj[i].restaurantConfirmation == False:
						flag = 0
				print(orderObj.Status)
				print(flag)
				if flag == 1:
					orderObj.Status = 2

			orderObj.save()
			status['acceptedOrderStatus'] = acceptedOrderNoList
		rejectedOrderNoList = request.data['rejectedOrderNoList']
		if rejectedOrderNoList == []:
			status['rejectedOrderStatus'] =  'no Orders are rejected'
		
		else:
			for i in rejectedOrderNoList:
				
				orderObj = Order.objects.get(orderNo = i)
				PermanentCartObj = PermanentCart.objects.filter(orderNo = i)

				for i in range(len(PermanentCartObj)):
					if PermanentCartObj[i].cartItem.res_id.res_user == request.user:

						print(PermanentCartObj[i].cartItem.res_id.name)
						PermanentCartObj[i].restaurantConfirmation = False
						PermanentCartObj[i].save()
					if PermanentCartObj[i].restaurantConfirmation == False:
						flag = 0
				print(orderObj.Status)
				print(flag)
				if flag == 1:
					orderObj.Status = 4

				orderObj.save()
				status['rejectedOrderStatus'] = rejectedOrderNoList
		return Response(status)
		