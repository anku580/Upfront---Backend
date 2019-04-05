from django.conf.urls import url
from .views.createPaymentRequestView import CreatePaymentRequestView
from .views.enterPaytmDetails  import enterPaytmDetails

urlpatterns = [
	url(r'^create/$',CreatePaymentRequestView.as_view(),name='create'),
	url(r'^paytm/details/$',enterPaytmDetails.as_view(),name='paytm_details'),

	# url(r'^done/$', views.payment_done, name= 'done'),
	# url(r'^canceled/$',views.payment_canceled,name='canceled'),
]