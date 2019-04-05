from  rest_framework.views import APIView
class EmailOrMobileNumber(APIView):
	def Post(self,request):
		ContactMedium = request.data['ContactMedium']
		

