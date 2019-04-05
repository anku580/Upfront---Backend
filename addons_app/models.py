# django imports
from django.db import models

# project imports
from restaurant_app.models import Restaurant


class RestaurantOffer(models.Model):
    res_id = models.ForeignKey(Restaurant,on_delete = models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    status = models.BooleanField(default = True)
    min_order_price = models.IntegerField()

class PromotionOffer(models.Model):
    offer_code = models.CharField(max_length=30)
    discount_percentage = models.FloatField()
    max_discount_price = models.IntegerField()
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    status = models.BooleanField(default = True)
    mode_of_payment = models.IntegerField()
    max_no_of_orders = models.IntegerField()
    min_order_price = models.IntegerField()
    min_time_difference = models.TimeField()

