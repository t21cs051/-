from django.urls import path
from . import views

app_name = "export"

urlpatterns = [
    path('export/measurement/', views.measurement_export, name='measurement_export'),
    path('export/worklog/', views.worklog_export, name='worklog_export'),
    path('export/ups/', views.ups_export, name='ups_export'),
    path('export/rack/', views.rack_export, name='rack_export'),
    path('export/powersystem/', views.powersystem_export, name='powersystem_export'),
]