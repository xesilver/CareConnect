from django.urls import path
from .views import SensorReadingListCreateView


urlpatterns = [
    path('api/v1/readings/', SensorReadingListCreateView.as_view(), name='sensorreading-list-create'),
]

