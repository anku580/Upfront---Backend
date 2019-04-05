
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime

# project imports
from tablebooking_app import custom_messages
from tablebooking_app.serializers import TableBookingSerializer
from tablebooking_app.models import TableBooking

class TableBookingView(APIView):

    def post(self,request,resid,tableid,dd,mm,yyyy):
        date = datetime.date(yyyy,mm,dd)
        json_response_obj = {}
        request.data['user_id'] = request.user.id
        request.data['date'] = date
        request.data['table_id'] = tableid
        tablebooking_serializer = TableBookingSerializer(data=request.data)
        if tablebooking_serializer.is_valid():
            tablebooking_serializer.save()
            json_response_obj['message'] = custom_messages.TABLE_RESERVED_SUCCESS_MSG
            json_response_obj['tablebooking'] = tablebooking_serializer.data
            return Response(json_response_obj)
        else:
            json_response_obj['message'] = tablebooking_serializer.errors
            return Response(json_response_obj)

    def get(self,request,resid,tableid,dd,mm,yyyy):
        date = datetime.date(yyyy,mm,dd)
        json_response_obj = {}
        all_tables = TableBooking.objects.filter(date=date)
        tablebooking_serializer = TableBookingSerializer(all_tables,many=True)
        json_response_obj['message'] = custom_messages.TABLE_BOOKING_DETAILS_RETRIVED_MSG
        json_response_obj['tablebookings'] = tablebooking_serializer.data
        return Response(json_response_obj)