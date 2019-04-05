from django.views.generic import TemplateView 

class PaypalButtonView(TemplateView):
	template_name = 'paypalbutton.html'
