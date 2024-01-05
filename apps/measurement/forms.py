from django import forms
from .models import CurrentMeasurement

class MeasurementIdForm(forms.Form):
    measurement_id = forms.IntegerField(label='ID')

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = CurrentMeasurement
        fields = ['measurement_date', 'current_value', 'power_system']

class MeasurementUpdateForm(forms.ModelForm):
    class Meta:
        model = CurrentMeasurement
        fields = ['measurement_date', 'current_value', 'power_system', 'employee']