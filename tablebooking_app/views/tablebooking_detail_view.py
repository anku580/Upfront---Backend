
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response

# project imports
from tablebooking_app.models import TableBooking
from tablebooking_app.serializers import TableBookingSerializer
from tablebooking_app import custom_messages
import datetime

class TableBookingDetailView(APIView):

    def put(self,request,resid,tableid,dd,mm,yyyy,bookingid):
        json_response_obj = {}
        request.data['user_id'] = request.user.id
        request.data['table_id'] = tableid
        request.data['date'] = datetime.date(yyyy,mm,dd)
        table_booking_obj = TableBooking.objects.get(id=bookingid)
        table_booking_serializer = TableBookingSerializer(table_booking_obj,data=request.data)
        if table_booking_serializer.is_valid():
            table_booking_serializer.save()
            json_response_obj['message'] = custom_messages.TABLE_BOOKING_UPDATED_SUCCESS_MSG
            json_response_obj['tablebooking'] = table_booking_serializer.data
            return Response(json_response_obj)
        else:
            json_response_obj['message'] = table_booking_serializer.errors
            return Response(json_response_obj)

    def get(self,request,resid,tableid,dd,mm,yyyy,bookingid):
        json_response_obj = {}
        table_booking_obj = TableBooking.objects.get(id=bookingid)
        table_booking_serializer = TableBookingSerializer(table_booking_obj)
        json_response_obj['message'] = custom_messages.TABLE_BOOKING_DETAILS_RETRIVED_MSG
        json_response_obj['tablebooking'] = table_booking_serializer.data
        return Response(json_response_obj)

    def delete(self,request,resid,tableid,dd,mm,yyyy,bookingid):
        json_response_obj = {}
        table_booking_obj = TableBooking.objects.get(id=bookingid)
        table_booking_obj.delete()
        json_response_obj['message'] = custom_messages.TABLE_BOOKING_CANCELLED_MSG
        return Response(json_response_obj)