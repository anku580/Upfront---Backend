from django.db import models
from  myuser.models import MyUser
from menu_app.models import Menu
from restaurant_app.models import Restaurant 


# # Create your models here.




class  FavoriteRestaurant(models.Model):
	favResUser = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	favRes = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.favResUser.username)

class  FavoriteMenu(models.Model):
	favMenuUser = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	favMenu = models.ForeignKey(Menu,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.favMenuUser.username)
