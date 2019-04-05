from rest_framework.serializers import ModelSerializer,ValidationError
from restaurant_app.models import Restaurant
from drf_extra_fields.fields import Base64ImageField

# DICTIONARY KEYS
LATITUDE = "latitude"
LONGITUDE = "longitude"

# ERROR MSGS
INVALID_LATITUDE_ERROR_MSG = "Invalid latitude value is passed"
INVALID_LONGITUDE_ERROR_MSG = "Invalid longitude value is passed"

class RestaurantSerializer(ModelSerializer):
    photo = Base64ImageField(represent_in_base64=False)
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate(self, attrs):
        if attrs[LATITUDE] >= 90 or attrs[LATITUDE] <= -90:
            raise ValidationError(INVALID_LATITUDE_ERROR_MSG)
        elif attrs[LONGITUDE] >= 180 or attrs[LONGITUDE] <= -180:
            raise ValidationError(INVALID_LONGITUDE_ERROR_MSG)
        return attrs

