from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()
import re

class Restaurant(models.Model):
    res_user = models.ForeignKey(User,on_delete=models.CASCADE,)
    name = models.CharField(max_length=50,)
    photo = models.ImageField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_activated = models.BooleanField(default=False)
    area = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    is_veg = models.BooleanField()
    approved_admin_id = models.ForeignKey(User,on_delete=models.PROTECT,related_name='approved_restaurants',null=True)

