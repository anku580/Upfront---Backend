from django.db import models

from temperorycart.models import Order
# Create your models here.

class Rating(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    rating = models.FloatField()
    msg = models.CharField(max_length=500)
