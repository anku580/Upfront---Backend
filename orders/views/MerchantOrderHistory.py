from rest_framework.views import APIView
from temperorycart.models import Order, PermanentCart
from restaurant_app.models import Restaurant
from menu_app.models import Menu
from rest_framework.response import Response
import json

class MerchantOrderHistory(APIView):
	def get(self,request):
		responseDict = {}
		orderNoList = []
		restaurantObj = Restaurant.objects.filter(res_user= request.user.id)
		for i in restaurantObj:
			menuObj = Menu.objects.filter(res_id = i.id)
			
			for j in menuObj:
				permanentCartObj  = PermanentCart.objects.filter(cartItem = j.id)
				for k in permanentCartObj:
					# print(k.orderNo)
					orderNoList.append(k.orderNo.id)
					if k.orderNo not in responseDict.keys():
						responseDict[k.orderNo.id] = {}
						responseDict[k.orderNo.id]['items'] = []
						responseDict[k.orderNo.id]['cost'] = 0
					responseDict[k.orderNo.id]['cost'] += k.itemCost
					responseDict[k.orderNo.id]['items'].append({k.cartItem.name:k.quantity})
		for i in orderNoList:
			orderObj = Order.objects.get(orderNo = i)
			print(orderObj)
			responseDict[i]['status'] = orderObj.Status
			responseDict[i]['initiatedTime'] = orderObj.orderCreatedTime.strftime("%I:%M:%S %p")
			if orderObj.ordercompleted == None:
				responseDict[i]['completedTime'] = 'order not completed'
			else:
				responseDict[i]['completedTime'] = orderObj.ordercompleted.strftime("%I:%M:%S %p")


		responseDict['status'] = 'successfull'
		# responseDict = json.dumps(responseDict)
		# print(responseDict)
		print(orderNoList)
		return Response(responseDict)
		
