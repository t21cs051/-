from django.contrib import admin
from apps.accounts.models import CustomUser

admin.site.register(CustomUser)
