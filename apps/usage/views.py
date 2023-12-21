import pandas as pd
from django_pandas.io import read_frame
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from apps.master.models import Rack
from apps.measurement.models import CurrentMeasurement

class UsageView(TemplateView):
    template_name = "usage/usage_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        measurement_queryset = CurrentMeasurement.objects.all()
        df_line = read_frame(measurement_queryset,
                            fieldnames=['measurement_date', 'current_value'])
        df_line['measurement_date'] = pd.to_datetime(df_line['measurement_date'])
        df_line['current_value'] = pd.to_numeric(df_line['current_value'])
        measurement_date = df_line['measurement_date'].tolist()
        current_value = df_line['current_value'].tolist()
        context['measurement_date'] = measurement_date
        context['current_value'] = current_value
        return context