from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser as Employee
from apps.master.models import PowerSystem
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import default

# 電流測定結果
class CurrentMeasurement(models.Model):
    measurement_date = models.DateTimeField(default=timezone.now) # 計測日時
    # TODO: 電流値の有効数字を指定する
    # 測定した電流値(0.0~100.0[A])
    current_value = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    # 計測対象の電源系統
    power_system = models.ForeignKey(PowerSystem, on_delete=models.CASCADE)

    # 計測者
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.current_value} [A]'