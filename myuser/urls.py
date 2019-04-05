from django.urls import path
from .views.testView import Testing 
from .views.customerView import CustomerRecordView
from .views.merchantView import MerchantRecordView
from .views.loginMerchantView import LoginMerchantAPIView
from .views.loginCustomerView import LoginCustomerAPIView
from .views.subadminView import  SubAdminRecordView
from rest_framework.urlpatterns import format_suffix_patterns
from .views.adminSignupView import adminSignupView
from .views.confirmAdminView import confirmAdminView
from .views.DeleteCustomerAccountView import DeleteCustomerAccountView
from .views.AdminDeleteAccountsView import AdminDeleteAccountsView

urlpatterns = [
   
    path('test/',Testing.as_view(),name="test"),
    path('signup/cust/',CustomerRecordView.as_view(),name="cust"),
    path('signup/merch/',MerchantRecordView.as_view(),name="merch"),
    path('signup/sub/',SubAdminRecordView.as_view(),name="sub"),
    path('signup/admin/',adminSignupView.as_view(),name="admin"),
    path('confirm/admin/',confirmAdminView.as_view(),name="confirm_admin"),


    path('login/merch/',LoginMerchantAPIView.as_view(),name="logmerch"),
    path('login/cust/',LoginCustomerAPIView.as_view(),name="logcust"),
    path('delete/cust/show/',DeleteCustomerAccountView.as_view(),name="logcust"),
    path('delete/cust/show/',AdminDeleteAccountsView.as_view(),name="logcust"),


]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])