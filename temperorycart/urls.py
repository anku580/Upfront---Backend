from django.urls import path
from .views.testView import Testing 

from .views.ShowCartView import CartViewSet

from .views.CartQuantityIncrementor import CartQuantityIncrementor
from .views.CartQuantityDecrementor import CartQuantityDecrementor
from .views.CartCreateBill import CartCreateBill
from .views.CartCreateOrder import CartCreateOrder
from .views.CustomizationMenu import CustomizationMenu

urlpatterns = [
   
    path('test/',Testing.as_view(),name="test"),

    path('item/add',CartViewSet.as_view(),name="add"),
    path('item/quantity/increase',CartQuantityIncrementor.as_view(),name="increase"),
    path('item/quantity/decrease',CartQuantityDecrementor.as_view(),name="decrease"),
    path('bill/',CartCreateBill.as_view(),name="bill"),
    # path('order/',CartCreateOrder.as_view(),name="order"),
    # path('order/<int:pk>',CartCreateOrder.as_view(),name="order1"),

    path('item/add/custom',CustomizationMenu.as_view(),name="customization"),




    path('show/',CartViewSet.as_view(),name="show"),



]