# django imports
from rest_framework.serializers import ModelSerializer
from drf_extra_fields.fields import Base64ImageField


# project imports
from menu_app.models import Category,Menu

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuSerializer(ModelSerializer):
    photo = Base64ImageField()
    class Meta:
        model = Menu
        fields = '__all__'

class MenuOfferSerializer(ModelSerializer):
    class Meta:
        model = Menu
        exclude = ('res_id','category_id')
        depth = 1
