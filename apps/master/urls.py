from django.urls import path
from .views import RackList,RackAddView,RackEditView,RackDeleteView
from .views import UpsList, UpsAddView, UpsEditView, UpsDeleteView
from .views import PowerSystemList, PowerSystemAddView, PowerSystemEditView, PowerSystemDeleteView, mainpage
from .views import EmployeeList, EmployeeEditView, EmployeeDeleteView, PasswordChangeView, PasswordChangeDoneView
from apps.accounts.views import EmployeeAddView
from .views import ExportView
from django.contrib.auth import views as auth_views 

app_name = "master"
urlpatterns = [
    path('main/', mainpage.as_view(), name='main'),
    path('rack/', RackList.as_view(), name='rack'),
    path('rack_add/', RackAddView.as_view(), name='rack_add'),
    path('rack_edit/<int:pk>/', RackEditView.as_view(), name='rack_edit'),
    path('rack_delete/<int:pk>/', RackDeleteView.as_view(), name='rack_delete'),
    path('ups/', UpsList.as_view(), name='ups'),
    path('ups_add/', UpsAddView.as_view(), name='ups_add'),
    path('ups_edit/<int:pk>/', UpsEditView.as_view(), name='ups_edit'),
    path('ups_delete/<int:pk>/', UpsDeleteView.as_view(), name='ups_delete'),
    path('power_system/', PowerSystemList.as_view(), name='power_system'),
    path('power_system_add/', PowerSystemAddView.as_view(), name='power_system_add'),
    path('power_system_edit/<int:pk>/', PowerSystemEditView.as_view(), name='power_system_edit'),
    path('power_system_delete/<int:pk>/', PowerSystemDeleteView.as_view(), name='power_system_delete'),
    path('employee/', EmployeeList.as_view(), name='employee'),
    path('employee_edit/<str:pk>/', EmployeeEditView.as_view(), name='employee_edit'),
    path('password_change_form/', PasswordChangeView.as_view(template_name='master/password_change.html'), name='password_change_form'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='master/password_change_done.html'), name='password_change_done'),
    path('employee_delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employee/add/', EmployeeAddView.as_view(), name='employee_add'),
    path('export/', ExportView.as_view(), name='export'),
]