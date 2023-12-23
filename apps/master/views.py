from apps.accounts.models import CustomUser as Employee
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Rack, Ups, PowerSystem
from .forms import RackIdForm, RackForm,UpsIdForm, UpsForm, PowerSystemIdForm, PowerSystemForm, EmployeeIdForm, EmployeeForm

#メインページ表示画面
class mainpage(TemplateView):
    template_name = 'master/master_main.html'
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('master:main'))


#ラック番号表示画面
class RackList(ListView):
    model = Rack
    template_name = 'master/rack_list.html'
    
    def post(self, request, *args, **kwargs):
        rack_id = self.request.POST.get('rack_id')
        rack = get_object_or_404(Rack, pk=rack_id)
        rack.save()
        return HttpResponseRedirect(reverse('master:rack'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        return context

class RackAddView(CreateView):
    model = Rack
    fields = ('rack_number',)
    template_name = 'master/rack_add.html'
    success_url = reverse_lazy('master:rack')


class RackEditView(UpdateView):
    model = Rack
    form_class = RackForm
    template_name = 'master/rack_edit.html'
    success_url = reverse_lazy('master:rack')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        return context

class RackDeleteView(DeleteView):
    model = Rack
    template_name = 'master/rack_delete.html'
    success_url = reverse_lazy('master:rack')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        return context
    
    
#UPS番号表示画面
class UpsList(ListView):
    model = Ups 
    template_name = 'master/ups_list.html'
    
    def post(self, request, *args, **kwargs):
        ups_id = self.request.POST.get('ups_id')
        ups = get_object_or_404(Ups, pk=ups_id)
        ups.save()
        return HttpResponseRedirect(reverse('master:ups'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UpsIdForm()
        return context
    
class UpsAddView(CreateView):
    model = Ups
    fields = ('ups_number',)
    template_name = 'master/ups_add.html'
    success_url = reverse_lazy('master:ups')

class UpsEditView(UpdateView):
    model = Ups
    form_class = UpsForm
    template_name = 'master/ups_edit.html'
    success_url = reverse_lazy('master:ups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UpsIdForm()
        return context

class UpsDeleteView(DeleteView):
    model = Ups
    template_name = 'master/ups_delete.html'
    success_url = reverse_lazy('master:ups')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UpsIdForm()
        return context
    

#電源系統表示画面
class PowerSystemList(ListView):
    model = PowerSystem
    template_name = 'master/power_system_list.html'
    
    def post(self, request, *args, **kwargs):
        power_system_id = self.request.POST.get('power_system_id')
        power_system = get_object_or_404(PowerSystem, pk=power_system_id)
        power_system.save()
        return HttpResponseRedirect(reverse('master:power_system'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = PowerSystemIdForm()
        return context
    
    
class PowerSystemAddView(CreateView):
    model = PowerSystem
    fields = ('power_system_number', 'max_current', 'supply_source', 'supply_rack')
    template_name = 'master/power_system_add.html'
    success_url = reverse_lazy('master:power_system')

class PowerSystemEditView(UpdateView):
    model = PowerSystem
    form_class = PowerSystemForm
    template_name = 'master/power_system_edit.html'
    success_url = reverse_lazy('master:power_system')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = PowerSystemIdForm()
        return context

class PowerSystemDeleteView(DeleteView):
    model = PowerSystem
    template_name = 'master/power_system_delete.html'
    success_url = reverse_lazy('master:power_system')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['power_system'] = self.get_object()
        context['form_id'] = PowerSystemIdForm()
        return context
    
#社員マスタ
class EmployeeList(TemplateView):
    model = Employee
    template_name = 'master/employee_list.html'
    
    def post(self, request, *args, **kwargs):
        employee_number = self.request.POST.get('employee_number')
        employee = get_object_or_404(Employee, pk=employee_number)
        employee.employee_number = employee_number
        employee.save()
        return HttpResponseRedirect(reverse('master:employee'))
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Employee.objects.all()
        return context
    
class EmployeeAddView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'master/employee_add.html'
    success_url = reverse_lazy('master:employee')

class EmployeeEditView(TemplateView):
    model = Employee
    fields = ('employee_number', 'full_name', 'password')
    template_name = 'master/employee_edit.html'
    success_url = 'employee/'

    def post(self, request, *args, **kwargs):
        employee_number = self.request.POST.get('employee_number')
        employee = get_object_or_404(Employee, pk=employee_number)
        form = EmployeeForm(request.POST, instance=employee)
        form.save()
        return HttpResponseRedirect(reverse('master:employee'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = EmployeeIdForm()
        context['form'] = EmployeeForm()
        return context
    
class EmployeeDeleteView(TemplateView):
    model = Employee
    template_name = 'master/employee_delete.html'
        
    def post(self, request, *args, **kwargs):
        employee_number = self.request.POST.get('employee_number')
        employee = get_object_or_404(Employee, pk=employee_number)
        employee.delete()
        return HttpResponseRedirect(reverse('master:employee'))

    def get_context_data(self, **kwargs):
        employee_number = self.request.POST.get('employee_number')
        employee = get_object_or_404(Employee, pk=employee_number)
        context = super().get_context_data(**kwargs)
        context['employee'] = employee
        context['form'] = EmployeeIdForm()
        return context
    