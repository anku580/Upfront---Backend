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
from .referral import produce_amount_keys
from .models import  ReferralModel
import base64
import json

import cgi

class CreateReferralView(APIView):
	permission_classes = (AllowAny,)
	def get(self,request):

		print(request.user)
		uniqueRandomString = ''
		status ={}
		flag = True
		try:
			referralObj =  ReferralModel.objects.get( sourceUser = request.user )
			status['referral' ] = {'url':'http://127.0.0.1:8000/referral/signup/cust/' + referralObj.referral}
		except  ReferralModel.DoesNotExist:

			while flag:
				try:
					uniqueRandomString = produce_amount_keys(1)
					referralObj =  ReferralModel.objects.get(referral= uniqueRandomString)
				except  ReferralModel.DoesNotExist:
					referralObj = ReferralModel(    sourceUser = request.user  ,referral = uniqueRandomString)
					referralObj.save()
					flag = False
			status['referral' ] = {'url':'http://127.0.0.1:8000/referral/signup/cust/' + uniqueRandomString}
		return Response(status['referral'])
		status['error'] = 'some error occured'
		return Response(status['error'])
	def put(self,request):

		print(request.user)
		uniqueRandomString = ''
		status = {}
		status['referral'] = {'string' :uniqueRandomString }
		flag = True
		while flag:
			try:
				uniqueRandomString = produce_amount_keys(1)
				referralObj =  ReferralModel.objects.get(referral= uniqueRandomString)
			except  ReferralModel.DoesNotExist:
				referralObj = ReferralModel.objects.get(sourceUser = request.user)
				referralObj.referral = uniqueRandomString


				referralObj.save()
				status['referral' ] = {'url':'http://127.0.0.1:8000/referral/signup/cust/' + referralObj.referral}

				flag = False
				return Response(status['referral'])
		status['error'] = 'some error occured'
		return Response(status['error'])
	def delete(self,request):

		print(request.user)
		uniqueRandomString = ''
		status = {}
		status['referral'] = {'string' :uniqueRandomString }
		flag = True
		while flag:
			try:
				uniqueRandomString = produce_amount_keys(1)
				referralObj =  ReferralModel.objects.get(referral= uniqueRandomString)
			except  ReferralModel.DoesNotExist:
				referralObj = ReferralModel.objects.get(sourceUser = request.user)
				referralObj.referral = uniqueRandomString


				referralObj.save()
				flag = False
				status['referral'] = {'status':'referral removed'}
				return Response(status['referral'])
		status['error'] = 'referral not deleted'
		return Response(status['error'])


