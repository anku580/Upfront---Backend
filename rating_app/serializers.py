
# django imports
from rest_framework.serializers import ModelSerializer

# project imports
from rating_app.models import Rating

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
