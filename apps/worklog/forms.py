
from django import forms
from .models import WorkLog

class WorkLogIdForm(forms.Form):
    worklog_id = forms.IntegerField(label='ID')

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['work_date', 'rack', 'work_type', 'description']
        widgets = {
            'work_date': forms.TextInput(attrs={'class': 'form-control'}),
            'rack': forms.Select(attrs={'class': 'form-select'}),
            'work_type': forms.RadioSelect(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            
        }


class WorkLogUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['work_date', 'rack', 'work_type', 'description', 'employee']
        widgets = {
            'work_date': forms.TextInput(attrs={'class': 'form-control'}),
            'rack': forms.Select(attrs={'class': 'form-select'}),
            'work_type': forms.RadioSelect(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),

        }