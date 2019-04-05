# django imports
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# project imports
from customization_app.models import Customization, MenuCustomization

class CustomizationSerializer(ModelSerializer):
    class Meta:
        model = Customization
        fields = '__all__'

        result = serializers.SerializerMethodField()

        def get_result(self, obj):
            return obj.result

class MenuCustomSerializer(ModelSerializer):
    class Meta:
        model = MenuCustomization
        fields = '__all__'




