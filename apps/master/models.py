from django.db import models

# ラックを表すモデル
class Rack(models.Model):
    rack_number = models.IntegerField() # ラック番号

    def __str__(self):
        return str(self.rack_number)
    
# UPSを表すモデル
class Ups(models.Model):
    ups_number = models.IntegerField() # UPS番号

    def __str__(self):
        return str(self.ups_number)

# 電源系統を表すモデル
class PowerSystem(models.Model):
    power_system_number = models.IntegerField() # 電源系統番号
    supply_source = models.ForeignKey(Ups, on_delete=models.CASCADE) # 電源供給元のUPS
    supply_rack = models.ForeignKey(Rack, on_delete=models.CASCADE) # 供給先のラック

    def __str__(self):
        return str(self.power_system_number)