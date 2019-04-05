from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.



class ReferralModel(models.Model):
    sourceUser = models.OneToOneField(User,on_delete=models.CASCADE)

    referral = models.CharField(unique = True,max_length=10,null = True)
    score = models.IntegerField(default = 0)
    
    def __str__(self):
       	return str(self.sourceUser)

