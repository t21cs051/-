from django.urls import path
from . import views

app_name = "worklog"

urlpatterns = [
    path('list/', views.WorkLogListView.as_view(), name='list'),
    path('add/', views.WorkLogAddView.as_view(), name='add'),
    path('update/<int:pk>/', views.WorkLogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.WorkLogDeleteView.as_view(), name='delete'),
]