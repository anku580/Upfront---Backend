from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import RegularModels
from menu_app.models import Menu
import datetime
import pytz


class RegularOrderView(APIView):
	def post(self,request):
		itemList = request.data['itemList']
		for i in itemList.keys():
			tz = pytz.timezone('GMT')
			currentDT = datetime.datetime.now(tz)
			currentDT  = currentDT + datetime.timedelta(hours=5,minutes = 30) 
			print(i,itemList[i],request.user.username)
			menuObj = Menu.objects.get(id = int(i))
			regularObj = RegularModels(	RegularOrderUser = request.user,item = menuObj ,quantity = itemList[i],created_time = currentDT )
			regularObj.save()
		return Response({request.user.username : itemList })

	def get(self,request):
		regularCart = {}
		regularObj = RegularModels.objects.filter(RegularOrderUser = request.user.id)
		for i in regularObj:
			regularCart[i.item.id] ={i.item.name:i.quantity}
		return Response(regularCart)


	def put(self,request):

		itemList = request.data['itemList']
		for i in itemList.keys():
			tz = pytz.timezone('GMT')
			currentDT = datetime.datetime.now(tz)
			currentDT  = currentDT + datetime.timedelta(hours=5,minutes = 30) 
			print(i,itemList[i],request.user.username)
			menuObj = Menu.objects.get(id = int(i))
			regularObj = RegularModels.objects.get(RegularOrderUser = request.user, item = menuObj)
			regularObj.quantity = itemList[i]
			regularObj.save()
		return Response({request.user.username : itemList })

	def delete(self,request):

		itemList = request.data['itemList']
		for i in itemList:
			
			menuObj = Menu.objects.get(id = i)
			regularObj = RegularModels.objects.get(RegularOrderUser = request.user, item = menuObj)
			regularObj.delete()
		return Response({request.user.username : itemList })






