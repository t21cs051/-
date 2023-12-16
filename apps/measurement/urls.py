from django.urls import path
from .views import MeasurementListView, MeasurementAddView, MeasurementShowView

app_name = "measurement"

urlpatterns = [
    
    path('', MeasurementListView.as_view(), name='measurement'),
    path('list/', MeasurementListView.as_view(), name='list'),
    path('add/', MeasurementAddView.as_view(), name='add'),
    path('show/', MeasurementShowView.as_view(), name='show'),
]