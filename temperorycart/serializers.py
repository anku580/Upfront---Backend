from rest_framework  import serializers  
from .models import Cart

from menu_app.models import Menu
from.models import Cart, PermanentCart,TotalCost, Order
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.validators import UniqueValidator

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart

        fields = ('id','itemId','quantity','user')

    def add_context(self):
        print(self.context)

class QuantityIncrementSerializer(serializers.Serializer):
	itemId = serializers.IntegerField()
	quantity = serializers.IntegerField()
	
class PermanentCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentCart
        fields = ('orderNo','cartUser','cartItem','itemCost','quantity')

class TotalCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalCost
        fields = ('Totalcost',)

class CompleteOrderSerializer(serializers.Serializer):
    items = PermanentCartSerializer(many=True)
    totalCost = TotalCostSerializer(many=True)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ( 'Status','Payment_type',)

