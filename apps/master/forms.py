from django import forms
from .models import Rack, Ups, PowerSystem
from apps.accounts.models import CustomUser as Employee

#ラック
class RackIdForm(forms.Form):
    rack_id = forms.IntegerField(label='rack_id')
    
class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['rack_number']
        
    
#UPS
class UpsIdForm(forms.Form):
    ups_id = forms.IntegerField(label='ups_id')
    
class UpsForm(forms.ModelForm):
    class Meta:
        model = Ups
        fields = ['ups_number']
    
#電源系統
class PowerSystemIdForm(forms.Form):
    power_system_id = forms.IntegerField(label='power_system_id')
    
class PowerSystemForm(forms.ModelForm):
    class Meta:
        model = PowerSystem
        fields = ['power_system_number', 'max_current', 'supply_source', 'supply_rack']
        
#社員マスタ
class EmployeeIdForm(forms.Form):
    employee_id = forms.IntegerField(label='employee_id')
    
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_number', 'full_name', 'password']