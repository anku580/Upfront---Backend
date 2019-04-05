from django.db import models

from menu_app.models import Menu
from restaurant_app.models import Restaurant
# Create your models here.

class Customization(models.Model):
    res_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE,)
    name = models.CharField(max_length=50)
    price = models.FloatField()

class MenuCustomization(models.Model):
    menu_id = models.ForeignKey(Menu,on_delete=models.CASCADE)
    customization_id = models.ForeignKey(Customization,on_delete=models.CASCADE)