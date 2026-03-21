from rest_framework import serializers


class CoordinateSerializer(serializers.Serializer):
    lat = serializers.FloatField(allow_null=True)
    lon = serializers.FloatField(allow_null=True)


class PopulationStatsSerializer(serializers.Serializer):
    total_population = serializers.IntegerField()
    land_area_sq_km = serializers.FloatField()
    density_per_sq_km = serializers.FloatField()


class GeoInsightSerializer(serializers.Serializer):
    country = serializers.CharField()
    capital = serializers.CharField(allow_null=True)
    region = serializers.CharField()

    coordinates = CoordinateSerializer()
    population_stats = PopulationStatsSerializer()

    flag = serializers.URLField(allow_null=True)