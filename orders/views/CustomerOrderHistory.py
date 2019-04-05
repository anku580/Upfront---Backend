from rest_framework.views import APIView
from rest_framework.response import Response
from temperorycart.models import Order, PermanentCart
class CustomerOrderHistory(APIView):
	def get(self,request):
		responseDict = {}
		orderObj = Order.objects.filter(orderUser= request.user.id)
		for i in orderObj:

			responseDict[i.orderNo.id] = {}
			responseDict[i.orderNo.id]['items'] = []
			responseDict[i.orderNo.id]['totalCost'] = i.totalcost
			responseDict[i.orderNo.id]['status'] = i.Status
			responseDict[i.orderNo.id]['initiatedTime'] = i.orderCreatedTime.strftime("%I:%M:%S %p")
			if i.ordercompleted == None:
				responseDict[i.orderNo.id]['completedTime'] = 'order not completed'
			else:
				responseDict[i.orderNo.id]['completedTime'] = i.ordercompleted.strftime("%I:%M:%S %p")
			permantCartObj = PermanentCart.objects.filter(orderNo = i.orderNo.id)
			for j in permantCartObj:
				responseDict[i.orderNo.id]['items'].append({j.cartItem.name:j.quantity})


		return Response(responseDict)



