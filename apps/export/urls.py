from django.urls import path
from . import views

app_name = "export"

urlpatterns = [
    path('export/', views.csv_export, name='csv_export'),
]