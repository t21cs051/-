from django.shortcuts import render
from django.views.generic.base import TemplateView
from apps.measurement.models import CurrentMeasurement
from apps.worklog.models import WorkLog

class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 電流測定データを取得
        measurement_queryset = CurrentMeasurement.objects.all().order_by('-measurement_date')

        # 作業記録データを取得
        worklog_queryset = WorkLog.objects.all().order_by('-work_date')

        # 測定データと作業記録を結合
        history_data = list(measurement_queryset) + list(worklog_queryset)
        history_data = history_data[:5]  # 最新5件

        # 日時でソート
        history_data.sort(key=lambda entry: entry.measurement_date if hasattr(entry, 'measurement_date') else entry.work_date, reverse=True)

        context['history_data'] = [
            {'employee': entry.employee if hasattr(entry, 'employee') else 'N/A',
             'content': '電流' if hasattr(entry, 'measurement_date') else '作業',
             'datetime': entry.measurement_date if hasattr(entry, 'measurement_date') else entry.work_date}
            for entry in history_data
        ]

        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'home/home.html', self.get_context_data())
