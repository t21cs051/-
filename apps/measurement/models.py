from django.db import models
from apps.accounts.models import CustomUser as Employee
from apps.master.models import PowerSystem

class CurrentMeasurement(models.Model):
    measurement_date = models.DateTimeField() # 計測日時
    # TODO: 電流値の有効数字を指定する
    current_value = models.FloatField() # 電流値
    power_system = models.ForeignKey(PowerSystem, on_delete=models.CASCADE) # 計測対象の電源系統
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) # 計測者