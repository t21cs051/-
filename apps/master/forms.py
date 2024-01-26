from django import forms
from .models import Rack, Ups, PowerSystem
from apps.accounts.models import CustomUser as Employee

#ラック
class RackIdForm(forms.Form):
    rack_number = forms.IntegerField(label='rack_number')
    
class RackForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)  # 説明は任意入力
    class Meta:
        model = Rack
        fields = ['rack_number', 'description']
        widgets = {
            'rack_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description == "":
            cleaned_data["description"] = ''
        return cleaned_data
    
#UPS
class UpsIdForm(forms.Form):
    ups_id = forms.IntegerField(label='ups_id')
    
class UpsForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)  # 説明は任意入力
    class Meta:
        model = Ups
        fields = ['ups_number', 'description']
        widgets = {
            'ups_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description == "":
            cleaned_data["description"] = ''
        return cleaned_data
    
#電源系統
class PowerSystemIdForm(forms.Form):
    power_system_id = forms.IntegerField(label='power_system_id')
    
class PowerSystemForm(forms.ModelForm):
    class Meta:
        model = PowerSystem
        fields = ['power_system_number', 'max_current', 'supply_source', 'supply_rack']
        widgets = {
            'power_system_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_current': forms.NumberInput(attrs={'class': 'form-control'}),
            'supply_source': forms.Select(attrs={'class': 'form-select'}),
            'supply_rack': forms.Select(attrs={'class': 'form-select'}),
        }
        
#社員マスタ
class EmployeeIdForm(forms.Form):
    employee_id = forms.IntegerField(label='employee_id')
    
class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ['employee_number', 'full_name']
        
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['employee_number'].widget.attrs['readonly'] = True
        
