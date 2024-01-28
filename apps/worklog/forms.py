
from django import forms
from .models import WorkLog

class WorkLogIdForm(forms.Form):
    worklog_id = forms.IntegerField(label='ID')

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'rack', 'work_type', 'description']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d %H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'rack': forms.Select(attrs={'class': 'form-select'}),
            # 'work_type': forms.RadioSelect(),
            'work_type': forms.HiddenInput(), # Bootstrapを使用するために、Djangoによるラジオボタンを隠す
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': '*必須* 作業内容を入力してください'}),
            
        }


class WorkLogUpdateForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['date', 'rack', 'work_type', 'description', 'employee']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d %H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'rack': forms.Select(attrs={'class': 'form-select'}),
            'work_type': forms.HiddenInput(), # Bootstrapを使用するために、Djangoによるラジオボタンを隠す
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),

        }