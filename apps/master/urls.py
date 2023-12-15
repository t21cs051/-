from django.urls import path
from .views import RackList,RackAddView, RackShowView,RackEditView,RackDeleteView, UpsList, PowerSystemList

app_name = "master"

urlpatterns = [
    path('rack/', RackList.as_view(), name='rack'),
    path('rack_add/', RackAddView.as_view(), name='rack_add'),
    path('rack_show/', RackShowView.as_view(), name='rack_show'),
    path('rack_edit/<int:id>/', RackEditView.as_view(), name='rack_edit'),
    path('rack_delete/<int:id>/', RackDeleteView.as_view(), name='rack_delete'),
    path('ups/', UpsList.as_view(), name='ups'),
    path('power_system/', PowerSystemList.as_view(), name='power_system'),
]