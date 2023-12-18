from django.shortcuts import render
from .models import CurrentMeasurement;
from .forms import MeasurementIdForm, MeasurementForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.base import reverse_lazy
# Create your views here.


class MeasurementListView(ListView):
    model = CurrentMeasurement;
    template_name = 'measurement/measurement_list.html'
    
    def post(self, request, *args, **kwargs):
        meaasurement_id = self.request.POST.get('measurement_id')
        measurement_date = self.request.POST.get('measurement_date');
        current_value = self.request.POST.get('current_value');
        power_system = self.request.POST.get('power_system');
        employee = self.request.POST.get('employee');
        CurrentMeasurement.save();
        return HttpResponseRedirect(reverse('measurement:measurement_list'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = MeasurementIdForm()
        return context

class MeasurementShowView(TemplateView):
    model = CurrentMeasurement;
    template_name = 'measurement/measurement_show.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = MeasurementIdForm()
        return context
    

class MeasurementAddView(CreateView):
    model = CurrentMeasurement;
    fields = ('measurement_date','current_value','power_system','employee');
    template_name = 'measurement/measurement_add.html'
    success_url = reverse_lazy('measurement:measurement_list')
    
    
    