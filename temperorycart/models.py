from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from restaurant_app.models import Restaurant
from menu_app.models import Menu
from rest_framework.decorators import action
from rest_framework import viewsets
from customization_app.models import Customization
# Create your models here.


class Cart(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	
	user = models.ForeignKey(User, related_name="carts",on_delete=models.CASCADE)


	itemId = models.ForeignKey(Menu,on_delete=models.CASCADE,null=True)


	quantity = models.IntegerField()
	
	updated_on = models.DateTimeField(auto_now=True)


	def __str__(self):
		return str(self.user) + ' ' + str(self.id)


class TotalCost(models.Model):
	Totalcost = models.FloatField()


class PermanentCart(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	orderNo = models.ForeignKey(TotalCost, related_name="cartuser",on_delete=models.CASCADE)

	cartUser = models.ForeignKey(User, related_name="cartuser",on_delete=models.CASCADE)
	cartItem = models.ForeignKey(Menu,on_delete=models.CASCADE,)    
	itemCost = models.FloatField()
	
	quantity = models.IntegerField()
	restaurantConfirmation = models.BooleanField(default = False)
	updated_on = models.DateTimeField(auto_now=True)


	def __str__(self):
		return str(self.cartUser)

class Order(models.Model):

	orderCreatedTime = models.DateTimeField(null = True)
	orderPaidTime = models.DateTimeField(null = True)
	orderRestaurantConfirmedTime  = models.DateTimeField(null = True)
	ordercompleted  = models.DateTimeField(null = True)
	orderUser = models.ForeignKey(User, related_name="orderuser",on_delete=models.CASCADE)
	STATUS_TYPE_CHOCES = (
		(1, 'intiated'),
		(2, 'processing'),
		(3, 'completed'),
		(4, 'rejected')
		)
	Status = models.PositiveSmallIntegerField(choices = STATUS_TYPE_CHOCES,default = 1)

	Payment_TYPE_CHOCES = (
		(1, 'Online Payment'),
		(2, 'Direct Payment'),
		)
	

	
	Payment_type = models.PositiveSmallIntegerField(choices = Payment_TYPE_CHOCES, null=True)
	paymentCompleted = models.BooleanField(default = False)
	orderNo = models.ForeignKey(TotalCost, related_name="total_cost",on_delete=models.CASCADE)
	totalcost = models.DecimalField(decimal_places = 2, max_digits = 7)



class BillModel(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	orderNo = models.ForeignKey(TotalCost, related_name="billorderno",on_delete=models.CASCADE)

	billuser = models.ForeignKey(User, related_name="billuser",on_delete=models.CASCADE)
	billResId = models.ForeignKey(Restaurant,on_delete=models.CASCADE,)    
	Cost = models.FloatField()

	
	
	updated_on = models.DateTimeField(auto_now=True)



	def __str__(self):
		return str(self.id)



class CartMenuCustomization(models.Model):
	customUser = models.ForeignKey(User, related_name="customuser",on_delete=models.CASCADE)
	# customization = models.ManyToManyField(Customization)
	menu_id = models.ForeignKey(Menu,on_delete = models.CASCADE)
	quantity = models.IntegerField()
	cartNo = models.ForeignKey(Cart, related_name="customorderno",on_delete=models.CASCADE)

class CustomizationOnQuantity(models.Model):
	cartMenuId = models.ForeignKey(CartMenuCustomization, related_name="custommenu",on_delete=models.CASCADE)
	customId = models.ForeignKey(Customization, related_name="cartmmenucustomisation",on_delete=models.CASCADE)


