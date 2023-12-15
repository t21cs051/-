from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from .models import WorkLog
from django.shortcuts import get_object_or_404
class WorkLogListView(ListView):
    model = WorkLog
    template_name = 'work_log/worklog_list.html'
    context_object_name = 'work_logs'
    paginate_by = 10
    # ordering = ['-created_at']


# WorkLogの追加ビュー
class WorkLogAddView(CreateView):
    model = WorkLog
    template_name = 'work_log/worklog_add.html'
    fields = ('work_date', 'rack', 'description', 'employee')
    success_url = '/work_log/' # 作成後に遷移するURL

class WorkLogUpdateView(UpdateView):
    model = WorkLog
    template_name = 'work_log/worklog_update.html'

    def post(self, request, *args, **kwargs):
        worklog_id = self.request.POST.get('workLog_id')
        date = self.request.POST.get('work_date')
        rack = self.request.POST.get('rack')
        description = self.request.POST.get('description')
        employee = self.request.POST.get('employee')

        worklog = get_object_or_404(WorkLog, pk=worklog_id)
        worklog.work_date = date
        worklog.rack = rack
        worklog.description = description
        worklog.employee = employee
        worklog.save()

        return HttpResponseRedirect(reverse('work_log:worklog_list'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context


