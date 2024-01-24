from django.shortcuts import render
from .models import CurrentMeasurement;
from .forms import MeasurementIdForm, MeasurementForm, MeasurementUpdateForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView,  UpdateView, DeleteView
from django.urls.base import reverse_lazy

class MeasurementListView(ListView):
    model = CurrentMeasurement
    template_name = 'measurement/measurement_list.html'

    def get_queryset(self):
        return CurrentMeasurement.objects.order_by('-measurement_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = MeasurementIdForm()
        return context
    
class MeasurementAddView(CreateView, ListView):
    model = CurrentMeasurement
    template_name = 'measurement/measurement_add.html'
    form_class = MeasurementForm
    success_url = reverse_lazy('measurement:add')

    def get_queryset(self):
        return CurrentMeasurement.objects.order_by('-id')[:8] # 直近の入力を上から8件まで表示
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = MeasurementIdForm()
        return context

class MeasurementUpdateView(UpdateView, ListView):
    model = CurrentMeasurement
    template_name = 'measurement/measurement_update.html'
    form_class = MeasurementUpdateForm
    success_url = reverse_lazy('measurement:list')

    def get_queryset(self):
        return CurrentMeasurement.objects.order_by('-measurement_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = MeasurementIdForm()
        return context
    
class MeasurementDeleteView(DeleteView):
    model = CurrentMeasurement
    template_name = 'measurement/measurement_delete.html'
    success_url = reverse_lazy('measurement:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = MeasurementIdForm()
        return context

    