from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.

class SendSms(View):
	def get(self,request):
		return redirect('https://www.fast2sms.com/dev/bulk?authorization=iTIxtsbkAm5B1eKUzulE8wyhjnWPvMd320Dq9QVNYCfJaHOo466xJy0OEvbQn2g9m5qu71jUY3AoawVG&sender_id=FSTSMS&message=hi dias this a test message from upfront&language=english&route=p&numbers=8111803626'
)
