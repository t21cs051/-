from django.urls import path
from .views import RackList, UpsList, PowerSystemList

app_name = "master"

urlpatterns = [
    path('rack/', RackList.as_view(), name='rack'),
    path('ups/', UpsList.as_view(), name='ups'),
    path('power_system/', PowerSystemList.as_view(), name='power_system'),
]