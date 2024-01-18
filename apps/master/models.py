from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ラックを表すモデル
class Rack(models.Model):
    # ラック番号(0~999)
    rack_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])

    # ラックの説明
    description = models.TextField(default='')

    def __str__(self):
        return str(self.rack_number)
    
# UPSを表すモデル
class Ups(models.Model):
    # UPS番号(0~99)
    ups_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])

    # UPSの説明
    description = models.TextField(default='')

    def __str__(self):
        return str(self.ups_number)

# 電源系統を表すモデル
class PowerSystem(models.Model):
    # 電源系統番号(0~999)
    power_system_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])

    # 電源系統の最大電流値(0.0~100.0[A])
    max_current = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    # 電源供給元のUPS
    supply_source = models.ForeignKey(Ups, on_delete=models.CASCADE)

    # 供給先のラック
    supply_rack = models.ForeignKey(Rack, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.power_system_number}: max[{self.max_current}]-from[{self.supply_source}]-to[{self.supply_rack}]'
    