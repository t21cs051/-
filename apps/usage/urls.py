from django.urls import path
from . import views

app_name = "usage"
urlpatterns = [
    path('main/', views.UsageView.as_view(), name='main'),
    path('graph/<int:rack_number>/', views.UsageGraphView.as_view(), name='graph'),
    path('graph/', views.UsageGraphView.as_view(), name='graph_no_rack_number'),
    path('graph/<int:rack_number>/<int:period>/', views.UsageGraphView.as_view(), name='graph'),
]