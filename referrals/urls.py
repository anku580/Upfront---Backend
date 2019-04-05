from django.conf.urls import url
from django.urls import path

from .views import CreateReferralView

from myuser.views.customerView import CustomerRecordView
from myuser.views.merchantView import MerchantRecordView

urlpatterns = [
	url(r'^create/$',CreateReferralView.as_view(),name='createreferral'),
	path('signup/cust/<str:referralString>',CustomerRecordView.as_view(),name="cust"),
    path('signup/merch/<str:referralString>',MerchantRecordView.as_view(),name="merch"),



	# url(r'^done/$', views.payment_done, name= 'done'),
	# url(r'^canceled/$',views.payment_canceled,name='canceled'),
]