from django.urls import path
from . import views

app_name = "work_log"

urlpatterns = [
    path('', views.WorkLogListView.as_view(), name='worklog_list'),
    path('add/', views.WorkLogAddView.as_view(), name='worklog_add'),
    path('update/', views.WorkLogUpdateView.as_view(), name='worklog_update'),
]