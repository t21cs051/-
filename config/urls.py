"""TD1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls'), name='accounts'),
    path('master/', include('apps.master.urls'), name='master'),
    path('data_export/', include('apps.data_export.urls'), name='data_export'),
    path('measurement/', include('apps.measurement.urls'), name='measurement'),
    path('usage_view/', include('apps.usage_view.urls'), name='usage_view'),
    path('worklog/', include('apps.worklog.urls'), name='worklog'),
]
