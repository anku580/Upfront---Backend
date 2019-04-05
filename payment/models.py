from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


# class BillModel(models.Model):
# 	date_created = models.DateTimeField(auto_now_add=True)
# 	orderNo = models.ForeignKey(TotalCost, related_name="cartuser",on_delete=models.CASCADE)

# 	billuser = models.ForeignKey(User, related_name="billuser",on_delete=models.CASCADE)
# 	billResId = models.ForeignKey(Restaurant,on_delete=models.CASCADE,)    
# 	Cost = models.FloatField()

	
	
# 	updated_on = models.DateTimeField(auto_now=True)



# 	def __str__(self):
# 		return str(self.id)


class PaytmDetails(models.Model):
	PaytmUser = models.OneToOneField(User,on_delete = models.CASCADE)
	PaytmId = models.CharField(max_length = 25)
	PaytmKey = models.CharField(max_length = 25)

	def __str__(self):
		return str(self.PaytmUser.username)