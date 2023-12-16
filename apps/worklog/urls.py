from django.urls import path
from . import views

app_name = "worklog"

urlpatterns = [
    path('list/', views.WorkLogListView.as_view(), name='worklog_list'),
    path('add/', views.WorkLogAddView.as_view(), name='worklog_add'),
    path('update/<int:pk>/', views.WorkLogUpdateView.as_view(), name='worklog_update'),
]