# import pandas as pd
# from django_pandas.io import read_frame
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count
from django.urls import reverse
from django.views.generic.base import TemplateView
from datetime import datetime, timedelta
from django.utils import timezone
from apps.master.models import Rack
from apps.measurement.models import CurrentMeasurement
from .forms import RackSelectForm, DateRangeForm

class UsageView(TemplateView):
    template_name = "usage/usage_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RackSelectForm()
        return context

class UsageGraphView(TemplateView):
    template_name = "usage/usage_graph.html"

    def get(self, request, *args, **kwargs):
        form = DateRangeForm()
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rack_number = self.request.GET.get('rack', '1')  # デフォルトのラック番号は1

        form = kwargs.get('form')
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] + timedelta(days=1)
        else:
            end_date = timezone.now().date() + timedelta(days=1)
            start_date = end_date - timedelta(days=31)
        
        # start_dateとend_dateをcontextに追加
        context['start_date'] = start_date
        context['end_date'] = end_date

        # power_systemごとにデータをグループ化
        power_systems = CurrentMeasurement.objects.values('power_system').annotate(count=Count('power_system')).order_by('power_system')

        data = {}
        for power_system in power_systems:
            measurement_queryset = CurrentMeasurement.objects.filter(
                power_system=power_system['power_system'], # 電源系統で絞り込み
                power_system__supply_rack=rack_number, # ラック番号で絞り込み
                measurement_date__range=(start_date, end_date) # 開始日と終了日の範囲で絞り込み
            ).order_by('measurement_date')
            # measurement_querysetが空でない場合にのみ、dataに追加
            if measurement_queryset.exists():
                data[power_system['power_system']] = [{'x': timezone.localtime(obj.measurement_date), 'y': obj.current_value} for obj in measurement_queryset]
        
        context['data'] = data
        
        return context
    