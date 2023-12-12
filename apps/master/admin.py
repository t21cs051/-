from django.contrib import admin
from apps.master.models import Rack, Ups, PowerSystem

admin.site.register(Rack)
admin.site.register(Ups)
admin.site.register(PowerSystem)
