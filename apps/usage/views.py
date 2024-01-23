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
from apps.worklog.models import WorkLog
from apps.usage.forms import RackSelectForm
from .forms import DateRangeForm

# 電源使用状況閲覧画面のメインビュー
class UsageView(TemplateView):
    template_name = "usage/usage_main.html"  # 使用するテンプレートを指定

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 親クラスのメソッドを呼び出して、コンテキストデータを取得
        racks = Rack.objects.all()  # すべてのRackを取得
        for rack in racks:  # 各Rackに対して
            power_systems = PowerSystem.objects.filter(supply_rack=rack)  # 現在のRackに供給しているPowerSystemを取得
            max_measurement = None  # 最大測定値を保存するための変数を初期化
            capacity = 0  # 定格電流を保存するための変数を初期化
            for power_system in power_systems:  # 各PowerSystemに対して
                # 現在のPowerSystemの最新の測定値を取得
                latest_measurement = CurrentMeasurement.objects.filter(power_system=power_system).order_by('-measurement_date').first()
                if latest_measurement is not None:  # 最新の測定値が存在する場合
                    # 最大測定値が未設定、または最新の測定値が現在の最大測定値より大きい場合
                    if max_measurement is None or latest_measurement.current_value > max_measurement:
                        max_measurement = latest_measurement.current_value  # 最大測定値を更新
                        capacity = power_system.max_current # 定格電流を更新
            # Rackの最大測定値を設定（最大測定値がNoneの場合は0を設定）
            rack.max_measurement = max_measurement if max_measurement is not None else 0
            rack.usage = round(max_measurement / capacity * 100, 1) if max_measurement is not None else 0  # Rackの使用率を設定
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

        period = self.kwargs.get('period') # 表示期間を取得

        # 表示期間に基づいて開始日と終了日を計算
        now = timezone.now().date()

        form = kwargs.get('form')
        if form.is_valid():
            print('フォームは有効です')
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] + timedelta(days=1)
        else: 
            if period == 1:
                start_date = now - timedelta(days=30)
            elif period == 3:
                start_date = now - timedelta(days=90)
            elif period == 6:
                start_date = now - timedelta(days=180)
            else:
                start_date = now - timedelta(days=30) # デフォルトは1か月
            end_date = now + timedelta(days=1)
        
        # start_dateとend_dateをcontextに追加
        context['start_date'] = start_date
        context['end_date'] = end_date

        # ラック番号をcontextに追加
        context['rack_number'] = rack_number

        # ラック番号でフィルタリングを行い、関連する電源系統を取得
        power_systems = PowerSystem.objects.filter(supply_rack=rack_number).values('power_system_number').order_by('power_system_number')

        # 各電源系統をキーとする辞書を初期化
        data = {power_system['power_system_number']: [] for power_system in power_systems}
        print(f'データ: {data}')

        max_currents = {}
        for power_system in power_systems:
            measurement_queryset = CurrentMeasurement.objects.filter(
                power_system=power_system['power_system_number'], # 電源系統で絞り込み
                power_system__supply_rack=rack_number, # ラック番号で絞り込み
                measurement_date__range=(start_date, end_date) # 開始日と終了日の範囲で絞り込み
            ).order_by('measurement_date')
            # querysetのデータを辞書に追加
            data[power_system['power_system_number']] = [{'x': timezone.localtime(obj.measurement_date), 'y': obj.current_value} for obj in measurement_queryset]
            max_currents[power_system['power_system_number']] = int(PowerSystem.objects.get(id=power_system['power_system_number']).max_current)
        context['data'] = data
        context['capacity'] = max_currents

        print(f'データ: {data}')
        
        # 指定された期間の作業履歴を取得
        worklogs = WorkLog.objects.filter(
            rack__rack_number=rack_number, # ラック番号で絞り込み
            work_date__range=(start_date, end_date) # 開始日と終了日の範囲で絞り込み
        ).order_by('work_date')

        # worklogsをcontextに追加
        worklogs_dict = {'設置': [], '撤去': [], 'その他': []}
        for obj in worklogs:
            worklogs_dict[obj.get_work_type_display()].append({'x': timezone.localtime(obj.work_date), 'y': obj.get_work_type_display(), 'z': obj.description.replace('\r\n', '').replace('\n', '')})
        context['worklogs'] = worklogs_dict

        return context
