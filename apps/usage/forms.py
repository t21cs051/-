
from django import forms
from datetime import datetime, timedelta
from apps.master.models import Rack

class RackSelectForm(forms.Form):
    rack = forms.ModelChoiceField(queryset=Rack.objects.all())


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='開始日', input_formats=['%Y-%m-%d'])
    end_date = forms.DateField(label='終了日', input_formats=['%Y-%m-%d'])

    def __init__(self, *args, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)
        today = datetime.now().date()
        last_month = today - timedelta(days=30)
        self.fields['start_date'].initial = last_month
        self.fields['end_date'].initial = today
