from django.contrib import admin

from .models import Cart, PermanentCart, TotalCost, PermanentCart, Order, BillModel, CartMenuCustomization, CustomizationOnQuantity

# Register your models here.

admin.site.register(Cart)
admin.site.register(TotalCost)
admin.site.register(PermanentCart)
admin.site.register(Order)
admin.site.register(BillModel)
admin.site.register(CartMenuCustomization)
admin.site.register(CustomizationOnQuantity)



