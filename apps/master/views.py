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
from django.template.context_processors import request
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin

#メインページ表示画面
class mainpage(TemplateView):
    template_name = 'master/master_main.html'
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('master:main'))


#ラック番号表示画面
class RackList(ListView):
    model = Rack
    template_name = 'master/rack_list.html'

    def get_queryset(self):
        return Rack.objects.order_by('rack_number')
    
    def post(self, request, *args, **kwargs):
        rack_number = self.request.POST.get('rack_number')
        rack = get_object_or_404(Rack, pk=rack_number)
        rack.save()
        return HttpResponseRedirect(reverse('master:rack'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        return context

class RackAddView(CreateView):
    model = Rack
    form_class = RackForm
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

    def get_queryset(self):
        return Ups.objects.order_by('ups_number')
    
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
    form_class = UpsForm
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

    def get_queryset(self):
        return PowerSystem.objects.order_by('power_system_number')
    
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
    form_class = PowerSystemForm
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
class EmployeeList(ListView):
    model = Employee
    template_name = 'master/employee_list.html'

    def get_queryset(self):
        return Employee.objects.order_by('employee_number')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ログイン中のユーザー情報を取得
        logged_in_user = self.request.user

        context['logged_in_user'] = logged_in_user
        return context


class EmployeeEditView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'master/employee_edit.html'
    success_url = reverse_lazy('master:employee')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログイン中のユーザー情報を取得
        logged_in_user = self.request.user
        context['logged_in_user'] = logged_in_user
        context['form_id'] = EmployeeForm(instance=logged_in_user)
        form = EmployeeForm(instance=logged_in_user)
        if form.is_valid():
            form.save()
        return context
    
    
class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'master/employee_delete.html'
    success_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログイン中のユーザー情報を取得
        logged_in_user = self.request.user
        context['logged_in_user'] = logged_in_user
        context['form_id'] = EmployeeForm(instance=logged_in_user)
        return context
    

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('master:password_change_done')
    template_name = 'master/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

class PasswordChangeDoneView(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'master/password_change_done.html'


class ExportView(TemplateView):
    template_name = 'master/export.html'