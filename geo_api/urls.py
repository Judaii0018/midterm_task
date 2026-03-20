from django.urls import path
from .views import GeoInsightView

urlpatterns = [
    path('v1/geo-insight/', GeoInsightView.as_view(), name='geo-insight-v1'),
]