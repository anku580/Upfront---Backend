from rest_framework.serializers import ModelSerializer
from tablebooking_app.models import Table,TableBooking

class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TableBookingSerializer(ModelSerializer):
    class Meta:
        model = TableBooking
        fields = '__all__'