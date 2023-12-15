from django import forms
from .models import Rack, Ups, PowerSystem

#ラック
class RackNumberForm(forms.Form):
    rack_number = forms.IntegerField(label='rack_number')
    
#UPS
class UpsNumberForm(forms.Form):
    ups_number = forms.IntegerField(label='ups_number')
    
#電源系統
class PowerSystemNumberForm(forms.Form):
    power_system_number = forms.IntegerField(label='power_system_number')
    
class PowerSystemForm(forms.ModelForm):
    class Meta:
        model = PowerSystem
        fields = ['max_current', 'supply_source', 'supply_rack']