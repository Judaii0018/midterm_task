from rest_framework import serializers

class CoordinateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

class PopulationStatsSerializer(serializers.Serializer):
    total_population = serializers.IntegerField()
    land_area_sq_km = serializers.FloatField()
    density_per_sq_km = serializers.FloatField()

class GeoInsightSerializer(serializers.Serializer):
    city = serializers.CharField()
    country = serializers.CharField()
    coordinates = CoordinateSerializer()
    population_stats = PopulationStatsSerializer()
    flag = serializers.URLField()