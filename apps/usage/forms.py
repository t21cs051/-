
from django import forms
from apps.master.models import Rack

class RackSelectForm(forms.Form):
    rack = forms.ModelChoiceField(queryset=Rack.objects.all())
