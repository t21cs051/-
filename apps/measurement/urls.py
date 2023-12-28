from django.urls import path
from .views import MeasurementListView, MeasurementAddView, MeasurementUpdateView, MeasurementDeleteView

app_name = "measurement"

urlpatterns = [
    path('list/', MeasurementListView.as_view(), name='list'),
    path('add/', MeasurementAddView.as_view(), name='add'),
    path('update/<int:pk>/', MeasurementUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MeasurementDeleteView.as_view(), name='delete'),
]