
"""upfront URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myuser/', include('myuser.urls')),
    path('paypal/',include('paypal.standard.ipn.urls')),
    url('payment/',include(('payment.urls','payment'),namespace='payment')),
    path('cart/', include('temperorycart.urls')),
    path('orders/', include('orders.urls')),
    path('restaurant/api/v1/',include('restaurant_app.urls')),
    path('menu/api/v1/',include('menu_app.urls')),
    path('tablebooking/api/v1/',include('tablebooking_app.urls')),
    path('addons/api/v1/',include('addons_app.urls')),
    path('sms/',include('SMS.urls')),
    path('orders/', include('orders.urls')),
    path('fav/', include('favourites.urls')),
    # path('email/',include('Email.urls')),
    path('referral/',include('referrals.urls')),
    path('customization/api/v1/',include('customization_app.urls'))



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)