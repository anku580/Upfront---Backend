from django.urls import path
from .views import SendSms

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
   
    path('send/',SendSms.as_view(),name="send"),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])