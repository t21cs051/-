from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser as Employee
from apps.master.models import Rack

class WorkLog(models.Model):
    work_date = models.DateTimeField(default=timezone.now()) # 作業日時
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE) # 作業対象のラック
    description = models.TextField() # 作業内容
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) # 作業者

    def __str__(self):
        return self.id