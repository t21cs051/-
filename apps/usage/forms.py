
from django import forms
from .models import Measurement, WorkLog, Rack

class WorkLogForm(forms.Form):
    model = WorkLog
