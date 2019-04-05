from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()
from myuser.models import Customer
from rest_framework.response import Response
from django.contrib.auth import authenticate



class AdminDeleteAccountsView(APIView):
	def get(self,request,userId = None):
		status = {}
		userObj = User.objects.get(id = userId)
		custObj = Customer.objects.get(customer = userObj)
		status['details'] = {
		'username':userObj.username,
		'email':custObj.custEmail,
		'mobNo':custObj.mobileNumber
		}
		return Response(status)
	def post(self,request,userId = None):
		status ={}
		username = request.data['username']
		password = request.data['password']
		
		user = authenticate(username=username, password=password)
		if(user is None):
			status['error'] = 'an user with the give usrname1 and password is not found'
		else:

			userObj = User.objects.get(id = userId)
			userObj.is_active = False
			userObj.save()
			status['success'] = 'the account was deleted'
		return Response(status) 
