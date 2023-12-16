from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import WorkLog
from django.shortcuts import get_object_or_404
from .models import WorkLog
from .forms import WorkLogIdForm, WorkLogForm

class WorkLogListView(ListView):
    model = WorkLog
    # template_name = 'worklog/worklog_list.html'
    # context_object_name = 'worklogs'
    # paginate_by = 10
    # # ordering = ['-created_at']
    def post(self, request, *args, **kwargs):
        worklog_id = self.request.POST.get('worklog_id')
        worklog = get_object_or_404(WorkLog, pk=worklog_id)
        worklog_status = self.request.POST.get('worklog_status')
        worklog.buy = worklog_status
        worklog.save()
        return HttpResponseRedirect(reverse('worklog:worklog_list'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context


# WorkLogの追加ビュー
class WorkLogAddView(CreateView):
    model = WorkLog
    template_name = 'worklog/worklog_add.html'
    fields = ('work_date', 'rack', 'work_type', 'description', 'employee')
    success_url = reverse_lazy('worklog:worklog_list')

# WorkLogの更新ビュー
class WorkLogUpdateView(UpdateView):
    model = WorkLog
    template_name = 'worklog/worklog_update.html'
    form_class = WorkLogForm  # YourWorkLogFormには、モデルに基づく適切なフォームが指定されていると仮定します
    success_url = reverse_lazy('worklog:worklog_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context
    
# WorkLogの削除ビュー
class WorkLogDeleteView(DeleteView):
    model = WorkLog
    template_name = 'worklog/worklog_delete.html'
    success_url = reverse_lazy('worklog:worklog_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context
