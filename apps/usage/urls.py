from django.urls import path
from . import views

app_name = "usage"
urlpatterns = [
    path('main/', views.UsageView.as_view(), name='main'),
    path('graph/<int:rack_id>/', views.UsageGraphView.as_view(), name='graph'),
    path('graph/', views.UsageGraphView.as_view(), name='graph_no_rack_id'),
    path('graph/<int:rack_id>/<int:period>/', views.UsageGraphView.as_view(), name='graph'),
]