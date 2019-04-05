from django.db import models
from restaurant_app.models import Restaurant
from addons_app.models import RestaurantOffer
import datetime

class Category(models.Model):
    res_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created_time = models.DateTimeField(auto_now_add=True,null=True)
    updated_time = models.DateTimeField(auto_now=True,null=True)

class Menu(models.Model):
    res_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    original_price = models.FloatField()
    discounted_price = models.FloatField(null=True)
    photo = models.ImageField()
    quantity = models.IntegerField()
    is_veg = models.BooleanField()
    rating = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True,null=True)
    updated_time = models.DateTimeField(auto_now=True,null=True)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    offer_id = models.ForeignKey(RestaurantOffer,on_delete=models.PROTECT,null=True)


