from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_country_insights   # ✅ updated import
from .serializers import GeoInsightSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter


class GeoInsightView(APIView):

    @extend_schema(
        summary="Get Country Insights",
        description="Retrieve country data and calculate population density using RestCountries API.",
        parameters=[
            OpenApiParameter(
                name='country',
                description='Name of the country (e.g., Philippines, Japan)',
                required=True,
                type=str
            )
        ],
        responses={200: GeoInsightSerializer}
    )
    def get(self, request):
        # ✅ Get country from query params
        country = request.query_params.get('country')

        if not country:
            return Response(
                {"error": "Please provide a 'country' query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Call updated service
        data = get_country_insights(country)

        if data is None:
            return Response(
                {"error": "Country not found or data unavailable."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Serialize response
        serializer = GeoInsightSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)