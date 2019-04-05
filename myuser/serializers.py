from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model
User = get_user_model()
from myuser.models import Customer,SubAdmin, Merchant

from django.contrib.auth import authenticate


# class UserRegistrationSerializer(serializers.Serializer):
# 	username = serializers.CharField(max_length=255)
# 	# id_no = serializers.CharField(max_length=15)
# 	# date_of_birth = serializers.DateField()
# 	customer = PrimaryKeyRelatedField(queryset=MyUserSerializer.objects.all(), validators=[<UniqueValidator(queryset=SnippetSerializer.objects.all())>])
# 	custEmail = EmailField(label='CustEmail', max_length=254)       
#     customerId = IntegerField(label='CustomerId', read_only=True)

# 	password = serializers.CharField(max_length=128)
# 	# phone_number = serializers.CharField(allow_blank=True, max_length=17, required=False, )
# 	# user_type = serializers.ChoiceField(allow_null=True, choices=((1, 'customer'), (2, 'merchant'), (3, 'sub_admin'), (4, 'admin')), required=False)
# 	password1 = serializers.CharField(max_length=128)

# 	def validate(self, data):
# 		if not data.get('password') or not data.get('password1'):

# 			raise serializers.ValidationError("Please enter a password and confirm it.")

# 		if data.get('password') != data.get('password1
# 			raise serializers.ValidationError("Those passwords don't match.")
# 			print("password donot match")
# 		else:
# 			print('passwords matches')
# 		return data

# class SnippetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ('customer','custEmail','customerId')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','token')


# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username','password','token')
   
 
    
class CustomerSerializer(serializers.ModelSerializer):
    """
    A subadmin customer to return the customer details
    """
    customer = UserSerializer(required=True)

    class Meta:
        model = Customer
        fields = ('customer','custEmail','mobileNumber')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('customer')
        customer = UserSerializer.create(UserSerializer(), validated_data=user_data)
        custom,created = Customer.objects.update_or_create(customer=customer,custEmail=validated_data.pop('custEmail'),mobileNumber=validated_data.pop('mobileNumber'))
        return customer


class SubAdminSerializer(serializers.ModelSerializer):
    """
    A subadmin serializer to return the subadmin details
    """
    subuser = UserSerializer(required=True)

    class Meta:
        model = SubAdmin
        fields = ('subuser','merchant','subEmail','mobileNumber')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('subuser')
        subuser = UserSerializer.create(UserSerializer(), validated_data=user_data)
        created = SubAdmin.objects.update_or_create(subuser=subuser, merchant=Merchant.objects.get(merchantId = validated_data.pop('merchant')), subEmail=validated_data.pop('subEmail'), mobileNumber=validated_data.pop('mobileNumber'))
        return subuser

class MerchantSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    merchant = UserSerializer(required=True)

    class Meta:
        model = Merchant

        fields = ('merchant','merchEmail','mobileNumber')


    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('merchant')
        merchant = UserSerializer.create(UserSerializer(), validated_data= user_data)
        merch,created = Merchant.objects.update_or_create(merchant=merchant,merchEmail=validated_data.pop('merchEmail'),mobileNumber=validated_data.pop('mobileNumber'))
        return merchant
    def make_merchant(self):
        
        hello = UserSerializer.make_merchant
        return hello



class LoginMerchantSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)


    def show_data(self,data):
        print(data)
        return data
    def validate1(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
       
        print(data.get('username'))

        username = data.get('username', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if username is None:
            raise serializers.ValidationError(
                'An username address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=username, password=password)
        
     

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )
        if user.is_merchant is False:
            raise serializers.ValidationError(
                'Only merchants can access this page'
            )
        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            
            'username': user.username,
            'is_merchant':user.is_merchant,
            'is_admin':user.is_admin,
            'token': user.token
        }




class LoginCustomerSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)


    def show_data(self,data):
        print(data)
        return data
    def validate1(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
       
        print(data.get('username'))

        username = data.get('username', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if username is None:
            raise serializers.ValidationError(
                'An username address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=username, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            
            'username': user.username,
            'is_merchant':user.is_merchant,
            'is_admin':user.is_admin,

            'token': user.token
        }

