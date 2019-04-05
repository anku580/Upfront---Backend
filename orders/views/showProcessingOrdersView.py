
from rest_framework.views import APIView
from temperorycart.models import Order
from orders.serializers import OrderRestaurantSerializer
from temperorycart.models import PermanentCart
from rest_framework.response import Response

class showProcessingOrdersView(APIView):
	def get(self,request, resId = None):
		orderObj = Order.objects.filter(Status = 2 )
		serializer  = OrderRestaurantSerializer(orderObj,many = True)
		restaurantOrderDict = {}
		tempDict = {}

		for l in serializer.data:
			for j in l:
				if j == 'orderNo':

					print('orderNo',l[j])
					PermanentCartObj = PermanentCart.objects.filter(orderNo = l[j])
					orderObj1 =Order.objects.get(orderNo = l[j])
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
						print(PermanentCartObj[i].cartItem.res_id.id,PermanentCartObj[i].orderNo.id,PermanentCartObj[i].cartItem.name,)
						# while flag == True:
						# tempDict[PermanentCartObj[i].orderNo.id][PermanentCartObj[i].cartItem.name] = PermanentCartObj[i].quantity
						
						restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['items'][PermanentCartObj[i].cartItem.name] =PermanentCartObj[i].quantity
							# if(PermanentCartObj[i].cartItem.name in restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id].keys()):
								# print(restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id].keys())
			

						restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['order_created'] =PermanentCartObj[i].date_created.strftime("%I:%M:%S %p")
						restaurantOrderDict[PermanentCartObj[i].cartItem.res_id.id][PermanentCartObj[i].orderNo.id]['status'] =orderObj1.Status

				# print('----- --------- ------- - - - -- -- - --- ---- -- -')

		print(restaurantOrderDict)
		print(tempDict)
		if resId == None:
			return Response(restaurantOrderDict)
		else:
			return Response(restaurantOrderDict[resId])
