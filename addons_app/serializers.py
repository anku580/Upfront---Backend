# django imports

from rest_framework.serializers import ModelSerializer

# project imports

from addons_app.models import RestaurantOffer,PromotionOffer

class RestaurantOfferSerializer(ModelSerializer):
    class Meta:
        model = RestaurantOffer
        fields = '__all__'

class AdminOfferSerializer(ModelSerializer):
    class Meta:
        model = PromotionOffer
        fields = '__all__'