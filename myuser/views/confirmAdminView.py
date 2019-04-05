from django.shortcuts import render

from django.http import HttpResponse
from myuser.serializers import UserSerializer
from myuser.models import ConfirmAdmin
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()



class confirmAdminView(APIView):

	permission_classes = (AllowAny,)

	def get(self,request):
		confirmObj = ConfirmAdmin.objects.filter(status = False)
		resultDict ={}
		count = 1
		resultDict['admin to be verified '+ str(count)]  = 'no admin to be verified'
		for i in confirmObj:
			tempDict = {'admin':i.admin.username, 'id':i.admin.id}
			resultDict['admin to be verified '+ str(count)]  = tempDict
			count = count + 1
		return Response(resultDict)

	def post(self, request):
		print (request.data)
		count = 1
		resultDict ={}
		resultDict['admin activated '+ str(count)]  = {'status':'no admin is activated'}
		for i in request.data['activateAdmins']:
			tempObj= User.objects.get(id=i['userId'])
			tempObj.is_admin=True
			tempObj.save()
			resultDict['admin activated '+ str(count)] = {'status': tempObj.username + ' is activated'}
			count += 1

		return Response(resultDict)
		