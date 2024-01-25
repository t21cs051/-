from django import forms
from .models import CurrentMeasurement

class MeasurementIdForm(forms.Form):
    measurement_id = forms.IntegerField(label='ID')

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = CurrentMeasurement
        fields = ['date', 'current_value', 'power_system']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'power_system': forms.Select(attrs={'class': 'form-select'}),
        }

class MeasurementUpdateForm(forms.ModelForm):
    class Meta:
        model = CurrentMeasurement
        fields = ['date', 'current_value', 'power_system', 'employee']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'power_system': forms.Select(attrs={'class': 'form-select'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
        }