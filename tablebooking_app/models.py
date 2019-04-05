from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from restaurant_app.models import Restaurant

User = get_user_model()

class Table(models.Model):
    resid = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    no = models.IntegerField()
    category = models.CharField(max_length=30)
    price_per_hour = models.IntegerField()
    no_of_seats = models.IntegerField()
    timing = models.CharField(max_length=30)

class TableBooking(models.Model):
    table_id = models.ForeignKey(Table,on_delete=models.PROTECT)
    user_id = models.ForeignKey(User,on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()