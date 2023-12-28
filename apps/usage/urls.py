from django.urls import path
from . import views

app_name = "usage"
urlpatterns = [
    path('main/', views.UsageView.as_view(), name='main'),
    path('graph/', views.UsageGraphView.as_view(), name='graph'),
]