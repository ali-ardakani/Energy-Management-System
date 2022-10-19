# views.py
import datetime as dt

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import DemandReport
from .serializers import DemandReportSerializer

properties = {
    'date': openapi.Schema(type=openapi.TYPE_STRING),
    'hour': openapi.Schema(type=openapi.TYPE_INTEGER),
    'market_demand': openapi.Schema(type=openapi.TYPE_INTEGER),
    'ontario_demand': openapi.Schema(type=openapi.TYPE_INTEGER),
    'market_peak_day': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    'ontario_peak_day': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    'market_peak_month': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    'ontario_peak_month': openapi.Schema(type=openapi.TYPE_BOOLEAN),
}


# It's a view that allows you to get, delete, and post to the DemandReport model
class DemandReportCreateView(generics.views.APIView):
    serializer_class = DemandReportSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response(
            description='Success',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties
                )
            )
                   },
        manual_parameters=[
            openapi.Parameter('start', openapi.IN_QUERY, description="Start date", type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="End date", type=openapi.TYPE_STRING)
            ],
        operation_summary="Get filtered demand reports",
        operation_description="It receives the following parameters in the query string: \n"\
                                "start, end\n"\
                                "It returns a list of demand reports.\n"\
                                "example: /api/demand?start=2021-01-01&end=2021-01-02\n"\
                                "Note: If no parameters are passed, it returns all the demand reports.\n"\
                                "Note: If only one parameter is passed, it returns all the demand reports from that date to the end or from the beginning to that date.\n"\
                                "Note: If the start date is greater than the end date, it returns an error.")
    def get(self, request, format=None):
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            if dt.datetime.strptime(start, '%Y-%m-%d') > dt.datetime.strptime(end, '%Y-%m-%d'):
                return Response({'error': 'The start date cannot be greater than the end date.'}, status=400)
            queryset = DemandReport.objects.filter(date__range=[start, end])
        elif start:
            queryset = DemandReport.objects.filter(date__gte=start)
        elif end:
            queryset = DemandReport.objects.filter(date__lte=end)
        else:
            queryset = DemandReport.objects.all()
        serializer = DemandReportSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(responses={200: "Deleted",
                                    400: "Bad request"},
                         operation_summary="Delete selected demand reports",
                         operation_description="It receives the following parameters in the query string: \n"\
                                                "date\n"
                                                "It deletes the demand reports from the date passed as a parameter.\n"\
                                                "example: /api/demand?date=2021-01-01\n"\
                                                "Note: If no parameters are passed, it returns an error.",
                         manual_parameters=[
                                openapi.Parameter('date', openapi.IN_QUERY, description="Date", type=openapi.TYPE_STRING)
                         ])
    def delete(self, request, format=None):
        date = request.GET.get('date')
        if not date:
            return Response({'error': 'The date parameter is required.'}, status=400)
        queryset = DemandReport.objects.filter(date=date)
        queryset.delete()
        return Response('Deleted')

    @swagger_auto_schema(responses={
        201: "Created",
        400: "Bad request"},
        operation_summary="Create a demand report",
        operation_description="It receives list of demand reports in the body of the request.\n"\
                                "example: /api/demand\n"\
                                "body: {\n"\
                                "    \"demand\": [\n"\
                                "    {\n"\
                                "        \"date\": \"2021-01-01\",\n"\
                                "        \"hour\": 1,\n"\
                                "        \"market_demand\": 100,\n"\
                                "        \"ontario_demand\": 100,\n"\
                                "    },\n"\
                                "    {\n"\
                                "        \"date\": \"2021-01-01\",\n"\
                                "        \"hour\": 2,\n"\
                                "        \"market_demand\": 200,\n"\
                                "        \"ontario_demand\": 200,\n"\
                                "    }\n"\
                                "    ]\n"\
                                "}\n"\
                                "Note: If the date, hour, market_demand, or ontario_demand fields are not passed, it returns an error.\n"\
                                "Note: If the date, hour, market_demand, or ontario_demand fields are not valid, it returns an error.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'demand': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'date': openapi.Schema(type=openapi.TYPE_STRING),
                            'hour': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'market_demand': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'ontario_demand': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                        )
                    )
                }
            )
        )         
    def post(self, request, format=None):
        serializer = DemandReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response("Created", status=201)
        return Response(serializer.errors, status=400)
