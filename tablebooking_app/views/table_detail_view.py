
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response

# project imports
from tablebooking_app.models import Table
from tablebooking_app.serializers import TableSerializer
from tablebooking_app import custom_messages

class TableDetailView(APIView):

    def put(self,request,resid,tableid):
        json_response_obj = {}
        request.data['resid'] = resid
        table_obj = Table.objects.get(id=tableid)
        table_serializer = TableSerializer(table_obj,data=request.data)
        if table_serializer.is_valid():
            table_serializer.save()
            json_response_obj['message'] = custom_messages.TABLE_UPDATED_SUCCESS_MSG
            json_response_obj['table'] = table_serializer.data
            return Response(json_response_obj)
        else:
            json_response_obj['message'] = table_serializer.errors
            return Response(json_response_obj)

    def get(self,request,resid,tableid):
        json_response_obj = {}
        table_obj = Table.objects.get(id=tableid)
        table_serializer = TableSerializer(table_obj)
        json_response_obj['message'] = custom_messages.TABLE_RETRIEVED_SUCCESS_MSG
        json_response_obj['tables'] = table_serializer.data
        return Response(json_response_obj)

    def delete(self,request,resid,tableid):
        json_response_obj = {}
        table_obj = Table.objects.get(id=tableid)
        table_obj.delete()
        json_response_obj['message'] = custom_messages.TABLE_DELETED_SUCCESS_MSG
        return Response(json_response_obj)