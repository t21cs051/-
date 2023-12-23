# import pandas as pd
# from django_pandas.io import read_frame
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from datetime import datetime, timedelta
from django.utils import timezone
from apps.master.models import Rack
from apps.measurement.models import CurrentMeasurement
from .forms import RackSelectForm

class UsageView(TemplateView):
    template_name = "usage/usage_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RackSelectForm()
        return context

class UsageGraphView(TemplateView):
    template_name = "usage/usage_graph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rack_number = self.request.GET.get('rack', '1')  # デフォルトのラック番号は1


        end_date = timezone.now() + timedelta(days=7) # 現在の日付の７日後を取得(開発用)
        start_date = timezone.now() - timedelta(days=7)  # 7日前の日付を取得

        # 条件にあった測定データを取得
        # 開始日：7日前
        # 終了日：現在の日付
        # ラック番号：1
        # 日付による昇順でソート
        measurement_queryset = CurrentMeasurement.objects.filter(
            power_system__supply_rack=rack_number, # 供給先ラック番号を指定
            measurement_date__range=(start_date, end_date) # データを取得する範囲を指定
        ).order_by('measurement_date') # 日付による昇順でソート

        # measurement_date = [obj.measurement_date for obj in measurement_queryset]
        # current_value = [obj.current_value for obj in measurement_queryset]
        # context['measurement_date'] = measurement_date
        # context['current_value'] = current_value
        data = [{'x': timezone.localtime(obj.measurement_date), 'y': obj.current_value} for obj in measurement_queryset]
        context['data'] = data
        print(data)
        return context
