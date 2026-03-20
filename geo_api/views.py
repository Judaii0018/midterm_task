from django.shortcuts import render

# Created views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_geo_insights
from .serializers import GeoInsightSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class GeoInsightView(APIView):

    @extend_schema(
        summary="Get Geographic Insights",
        description="Combines Location API and Population API data to provide density metrics.",
        parameters=[
            OpenApiParameter(name='target', description='IP Address or Domain', required=True, type=str)
        ],
        responses={200: GeoInsightSerializer}
    )
    def get(self, request):
        # Retrieve the 'target' query parameter (e.g., ?target=google.com)
        target = request.query_params.get('target')

        if not target:
            return Response(
                {"error": "Please provide a 'target' query parameter (IP or domain)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the service logic from Phase 3
        data = get_geo_insights(target)

        if data is None:
            return Response(
                {"error": "Could not retrieve data for the provided target."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the data and return it
        serializer = GeoInsightSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)