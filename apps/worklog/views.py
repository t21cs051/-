from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import WorkLog
from django.shortcuts import get_object_or_404
from .models import WorkLog
from .forms import WorkLogIdForm, WorkLogForm

class WorkLogListView(ListView):
    model = WorkLog
    template_name = 'worklog/worklog_list.html'
    context_object_name = 'worklogs'
    paginate_by = 10
    # ordering = ['-created_at']


# WorkLogの追加ビュー
class WorkLogAddView(CreateView):
    model = WorkLog
    template_name = 'worklog/worklog_add.html'
    fields = ('work_date', 'rack', 'description', 'employee')
    success_url = '/worklog/' # 作成後に遷移するURL

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
