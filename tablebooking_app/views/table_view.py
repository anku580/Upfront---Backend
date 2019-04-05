
# django imports
from rest_framework.views import APIView
from rest_framework.response import Response

# project imports
from tablebooking_app import custom_messages
from tablebooking_app.serializers import TableSerializer
from tablebooking_app.models import Table

class TableView(APIView):

    def post(self,request,resid):
        json_response_obj = {}
        request.data['resid'] = resid
        table_serializer = TableSerializer(data=request.data)
        if table_serializer.is_valid():
            table_serializer.save()
            json_response_obj['message'] = custom_messages.TABLE_CREATED_SUCCESS_MSG
            json_response_obj['table'] = table_serializer.data
            return Response(json_response_obj)
        else:
            json_response_obj['message'] = table_serializer.errors
            return Response(json_response_obj)

    def get(self,request,resid):
        json_response_obj = {}
        all_tables = Table.objects.filter(resid=resid)
        table_serializer = TableSerializer(all_tables,many=True)
        json_response_obj['message'] = custom_messages.TABLE_RETRIEVED_SUCCESS_MSG
        json_response_obj['tables'] = table_serializer.data
        return Response(json_response_obj)