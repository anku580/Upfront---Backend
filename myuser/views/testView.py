from django.http import HttpResponse
from django.views.generic import View 

class Testing(View):
	def get (self, request):

		return HttpResponse("<html><body>Testing Successfull</body></html>")