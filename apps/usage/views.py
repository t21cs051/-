# import pandas as pd
# from django_pandas.io import read_frame
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Count, Max
from django.urls import reverse
from django.views.generic.base import TemplateView
from datetime import datetime, timedelta
from django.utils import timezone
from apps.master.models import Rack, PowerSystem
from apps.measurement.models import CurrentMeasurement
from .forms import RackSelectForm, DateRangeForm

# 電源使用状況閲覧画面のメインビュー
class UsageView(TemplateView):
    template_name = "usage/usage_main.html"  # 使用するテンプレートを指定

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 親クラスのメソッドを呼び出して、コンテキストデータを取得
        racks = Rack.objects.all()  # すべてのRackを取得
        for rack in racks:  # 各Rackに対して
            power_systems = PowerSystem.objects.filter(supply_rack=rack)  # 現在のRackに供給しているPowerSystemを取得
            max_measurement = None  # 最大測定値を保存するための変数を初期化
            for power_system in power_systems:  # 各PowerSystemに対して
                # 現在のPowerSystemの最新の測定値を取得
                latest_measurement = CurrentMeasurement.objects.filter(power_system=power_system).order_by('-measurement_date').first()
                if latest_measurement is not None:  # 最新の測定値が存在する場合
                    # 最大測定値が未設定、または最新の測定値が現在の最大測定値より大きい場合
                    if max_measurement is None or latest_measurement.current_value > max_measurement:
                        max_measurement = latest_measurement.current_value  # 最大測定値を更新
            # Rackの最大測定値を設定（最大測定値がNoneの場合は0を設定）
            rack.max_measurement = max_measurement if max_measurement is not None else 0
        context['racks'] = racks  # コンテキストデータにRackのリストを追加
        return context  # コンテキストデータを返す

# 電源使用状況グラフのビュー
class UsageGraphView(TemplateView):
    template_name = "usage/usage_graph.html"

    def get(self, request, *args, **kwargs):
        form = DateRangeForm()
        rack_select_form = RackSelectForm()
        context = self.get_context_data(form=form, rack_select_form=rack_select_form)
        context['rack_id'] = kwargs['rack_id']  # ラックIDを取得
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rack_number = self.kwargs['rack_id']  # URL引数からラック番号を取得

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

        # ラック番号をcontextに追加
        context['rack_number'] = rack_number

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
        print(start_date, end_date)
        
        return context
    