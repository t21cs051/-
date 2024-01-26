from django.shortcuts import render
from django.views.generic.base import TemplateView
from apps.measurement.models import CurrentMeasurement
from apps.worklog.models import WorkLog
from apps.master.models import Rack, PowerSystem

class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 電流測定データを取得
        measurement_queryset = CurrentMeasurement.objects.all().order_by('-date')[:10]

        # 作業記録データを取得
        worklog_queryset = WorkLog.objects.all().order_by('-date')[:10]

        # 測定データと作業記録を結合
        combined_data = (list(worklog_queryset) + list(measurement_queryset))[:10]

        # 日時でソート
        combined_data.sort(key=lambda entry: entry.date if hasattr(entry, 'date') else entry.date, reverse=True)

        context['combined_data'] = [
            {
                'employee': entry.employee if hasattr(entry, 'employee') else 'N/A',
                'type': '電流' if isinstance(entry, CurrentMeasurement) else '作業',
                'datetime': entry.date,
                'content': f'系統{entry.power_system}: {entry.current_value}A' if isinstance(entry, CurrentMeasurement) else f'ラック{entry.rack}: {entry.get_work_type_display()}' if isinstance(entry, WorkLog) else 'N/A',
            }
            for entry in combined_data
        ]

        racks = Rack.objects.all()
        for rack in racks:
            power_systems = PowerSystem.objects.filter(supply_rack=rack)
            max_measurement = None
            capacity = 0
            for power_system in power_systems:
                latest_measurement = CurrentMeasurement.objects.filter(power_system=power_system).order_by('-date').first()
                if latest_measurement is not None:
                    if max_measurement is None or latest_measurement.current_value > max_measurement:
                        max_measurement = latest_measurement.current_value
                        capacity = power_system.max_current
            rack.max_measurement = max_measurement if max_measurement is not None else 0
            rack.usage = round(max_measurement / capacity * 100, 1) if max_measurement is not None else 0

        context['racks'] = racks

        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'home/home.html', self.get_context_data())
    
class LogView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 電流測定データを取得
        measurement_queryset = CurrentMeasurement.objects.all().order_by('-date')

        # 作業記録データを取得
        worklog_queryset = WorkLog.objects.all().order_by('-date')

        # 測定データと作業記録を結合
        history_data = list(measurement_queryset) + list(worklog_queryset)
        history_data = history_data[:5]  # 最新5件

        # 日時でソート
        history_data.sort(key=lambda entry: entry.date if hasattr(entry, 'date') else entry.date, reverse=True)

        context['history_data'] = [
            {'employee': entry.employee if hasattr(entry, 'employee') else 'N/A',
             'content': '電流' if hasattr(entry, 'date') else '作業',
             'datetime': entry.date if hasattr(entry, 'date') else entry.date}
            for entry in history_data
        ]

        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'home/home.html', self.get_context_data())
