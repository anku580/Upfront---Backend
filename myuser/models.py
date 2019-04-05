from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

from time import time
from django.conf import settings
import jwt

# Create your models here.
class MyuserManager(BaseUserManager):

	def create_user(self, username,  password=None,is_customer=True,is_merchant=False,is_subadmin=False):
		""" Creates and saves a User with the given email, date of birtb and password."""
		if not username:
			raise ValueError('users must have an username')

		user = self.model(
			username = username,
			is_customer=is_customer,
			is_merchant =is_merchant,
			is_subadmin=is_subadmin,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password,is_customer=True,is_merchant=True,is_subadmin=False):
		"""
		creates and save a superuser with the given email, date of birth and password.
		"""

		user = self.create_user(
			username = username,
			password = password,
			is_merchant = is_merchant,
			is_customer = is_customer,
			is_subadmin=is_subadmin,
			)

		user.is_admin=True
		user.save(using = self.db)
		return user

class MyUser(AbstractBaseUser):
	username = models.CharField(
		verbose_name = 'username',
		max_length=255,
		unique = True,
		null = False,
		)
	

	# USER_TYPE_CHOCES = (
	# 	(1, 'customer'),
	# 	(2, 'merchant'),
	# 	(3, 'sub_admin'),
	# 	(4,'admin'),
	# 	)

	# user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOCES, null=True)
	# date_of_birth = models.DateField()
	# id_no = models.CharField(max_length=15)
	# phone_regex = RegexValidator(regex=r'^[9,8,7,6]\d{9}$', message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")
	# phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	# Created_on = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default =True)
	is_admin = models.BooleanField(default = False)
	is_customer = models.BooleanField(default =True)
	is_merchant = models.BooleanField(default = False)
	is_subadmin= models.BooleanField(default=False)


	objects = MyuserManager()

	USERNAME_FIELD = 'username'
	# REQUIRED_FIELDS = ['date_of_birth','id_no', 'phone_number']


	def __str__(self):
		return self.username


	@property
	def token(self):
		"""
		Allows us to get a user's token by calling `user.token` instead of
		`user.generate_jwt_token().

		The `@property` decorator above makes this possible. `token` is called
		a "dynamic property".
		"""
		return self._generate_jwt_token()

	def get_short_name(self):
	# The user is identified by their username
		return self.username
	def _generate_jwt_token(self):
		"""
		Generates a JSON Web Token that stores this user's ID and has an expiry
		date set to 60 days into the future.
		"""

		

		token = jwt.encode({
			'id': self.pk,
			'exp':time() + 3000
		}, settings.SECRET_KEY, algorithm='HS256')


		return token.decode('utf-8')

	def has_perm(self, perm, obj=None):
		#Does user has a specification permission

		return True

	def has_module_perms(self,perm,obj=None):

		return True
	def  make_merchant(cls,is_merchant):
		MyUser = cls(is_merchant = True)
		return MyUser
	@property
	def is_staff(self):
		"""
		IS the user a member of staff
		"""
		return self.is_admin
	def __str__(self):
		return self.username


class Customer(models.Model):
	customer = models.OneToOneField(MyUser,on_delete=models.CASCADE)
	custEmail = models.EmailField(null = True)
	customerId = models.AutoField(primary_key=True)
	mobileNumber = models.BigIntegerField(
        #if you want that field to be mandatory
        validators=[
            RegexValidator(
                regex='^[6-9]\d{9}$',
                message='Hashtag doesnt comply',
            ),
        ],null = True
    )

	def __str__(self):
		return self.customer.username



class Merchant(models.Model):

	merchant = models.OneToOneField(MyUser,on_delete=models.CASCADE,
       )
	merchEmail = models.EmailField(null = True)
	merchantId = models.AutoField(primary_key=True)
	mobileNumber = models.BigIntegerField(
        #if you want that field to be mandatory
        validators=[
            RegexValidator(
                regex='^[6-9]\d{9}$',
                message='Hashtag doesnt comply',
            ),
        ],null = True
    )

	def __str__(self):
		return str(self.merchant.username) + ' ' + str(self.merchantId)



class SubAdmin(models.Model):
	subuser = models.OneToOneField(MyUser,on_delete=models.CASCADE) 

	merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE,)
	# merchant_name = models.CharField(max_length=100)

	subEmail = models.EmailField(null = True)
	mobileNumber = models.BigIntegerField(
        #if you want that field to be mandatory
        validators=[
            RegexValidator(
                regex='^[6-9]\d{9}$',
                message='Hashtag doesnt comply',
            ),
        ],null = True
    )



class ConfirmAdmin(models.Model):
	created_time = models.DateTimeField(auto_now_add = True)
	admin = models.OneToOneField(MyUser,related_name='adminUser',on_delete=models.CASCADE)
	approved_admin = models.ForeignKey(MyUser,related_name ='approved_admin',on_delete=models.CASCADE,null =True)
	status = models.BooleanField(default=False)
	updated_time =models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.admin.username)

class ContactMedium(models.Model):
	user = models.OneToOneField(MyUser,related_name='contactUser',on_delete=models.CASCADE)
	Contact_TYPE_CHOCES = (
		(1, 'Email'),
		(2, 'MobileNumber'),
		)
	Contact_type = models.PositiveSmallIntegerField(choices = Contact_TYPE_CHOCES, null=True)	


