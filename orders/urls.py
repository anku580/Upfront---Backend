from django.urls import path
from .views.testView import Testing 

from .views.paypalView import PaypalButtonView
from .views.orderResponseView import OrderResponseView
from . views.RestaurantOrderConfirmationView import RestaurantOrderConfirmationView
from .views.restaurantOrdersListView import restaurantOrdersListView
from .views.showProcessingOrdersView import showProcessingOrdersView
from .views.MerchantOrderHistory import MerchantOrderHistory
from .views.CustomerOrderHistory import CustomerOrderHistory
from . views.RegularOrderView import RegularOrderView

urlpatterns = [
   
    path('test/',Testing.as_view(),name="test"),

    path('button/',PaypalButtonView.as_view(),name="button"),
    path('response/',OrderResponseView.as_view(),name="response"),
    path('restaurant/confirmation',RestaurantOrderConfirmationView.as_view(),name="confirmation"),
    path('restaurant/confirmation/<int:resId>',RestaurantOrderConfirmationView.as_view()),
    path('restaurant/show/initiated',restaurantOrdersListView.as_view(),name = 'res_show'),
    path('restaurant/show/initiated/<int:resId>',restaurantOrdersListView.as_view(),name = 'res_show'),
    path('restaurant/show/processing/<int:resId>',showProcessingOrdersView.as_view(),name = 'res_show'),
    path('restaurant/show/processing',showProcessingOrdersView.as_view(),name = 'res_show'),
    path('restaurant/show/merch/history',MerchantOrderHistory.as_view(),name = 'res_show'),
    path('restaurant/show/cust/history',CustomerOrderHistory.as_view(),name = 'res_show'),
    path('regular/add',RegularOrderView.as_view(),name = 'add_regular_order'),

    # path('restaurant')

]