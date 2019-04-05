from rest_framework  import serializers  


from menu_app.models import Menu
from temperorycart.models import Cart, PermanentCart,TotalCost, Order
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.validators import UniqueValidator
from temperorycart.serializers import PermanentCartSerializer


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ( 'Status','Payment_type','Orderuser','orderNo','totalcost')
