from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser as Employee
from apps.master.models import Rack

class WorkLog(models.Model):
    # 作業種別を列挙
    WORK_TYPES = [
        ('installation', '設置'),
        ('removal', '撤去'),
        ('other', 'その他'),
    ]

    work_date = models.DateTimeField(default=timezone.now) # 作業日時
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE) # 作業対象のラック
    work_type = models.CharField(max_length=20, choices=WORK_TYPES, default="installation") # 作業種別
    description = models.TextField() # 作業内容
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) # 作業者

    def __str__(self):
        return self.id