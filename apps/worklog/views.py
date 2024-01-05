from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import WorkLog
from django.shortcuts import get_object_or_404
from .models import WorkLog
from .forms import WorkLogIdForm, WorkLogForm, WorkLogUpdateForm

class WorkLogListView(ListView):
    model = WorkLog
    def post(self, request, *args, **kwargs):
        worklog_id = self.request.POST.get('worklog_id')
        worklog = get_object_or_404(WorkLog, pk=worklog_id)
        worklog_status = self.request.POST.get('worklog_status')
        # worklog.buy = worklog_status
        worklog.save()
        return HttpResponseRedirect(reverse('worklog:list'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context


# WorkLogの追加ビュー
class WorkLogAddView(CreateView):
    model = WorkLog
    template_name = 'worklog/worklog_add.html'
    form_class = WorkLogForm
    success_url = reverse_lazy('worklog:list')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context

# WorkLogの更新ビュー
class WorkLogUpdateView(UpdateView, ListView):
    model = WorkLog
    template_name = 'worklog/worklog_update.html'
    form_class = WorkLogUpdateForm
    success_url = reverse_lazy('worklog:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context
    
# WorkLogの削除ビュー
class WorkLogDeleteView(DeleteView):
    model = WorkLog
    template_name = 'worklog/worklog_delete.html'
    success_url = reverse_lazy('worklog:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = WorkLogIdForm()
        return context
