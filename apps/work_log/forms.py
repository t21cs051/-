
from django import forms
from .models import WorkLog

class WorkLogIdForm(forms.Form):
    worklog_id = forms.IntegerField(label='ID')

class ItemForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['work_date', 'rack', 'description', 'employee']