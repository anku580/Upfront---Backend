from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()
from myUser.models import Merchant
from rest_framework.response import Response
from django.contrib.auth import authenticate



class DeleteMerchantountView(APIView):
	def get(self,request):
		status = {}
		userObj = User.objects.get(id = request.user.id)
		merchObj = Merchant.objects.get(customer = userObj)
		status['details'] = {
		'username':userObj.username,
		'email':merchObj.custEmail,
		'mobNo':merchObj.mobileNumber
		}
		return Response(status)
	def post(self,request):
		status ={}
		username = request.data['username']
		password = request.data['password']
		
		user = authenticate(username=username, password=password)
		if(user is None):
			status['error'] = 'an user with the give usrname1 and password is not found'
		else:

			userObj = User.objects.get(id = request.user.id)
			userObj.is_active = False
			userObj.save()
			status['success'] = 'the account was deleted'
		return Response(status) 