from django import forms
from .models import Rack, Ups

#ラック
class RackNumberForm(forms.Form):
    rack_number = forms.IntegerField(label='rack_number')
    
#UPS
class UpsNumberForm(forms.Form):
    ups_number = forms.IntegerField(label='ups_number')
