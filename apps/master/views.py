from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Rack, Ups, PowerSystem
from .forms import RackIdForm, RackForm,UpsIdForm, UpsForm, PowerSystemIdForm, PowerSystemForm

#メインページ表示画面
class mainpage(TemplateView):
    template_name = 'master/master_main.html'
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('master:main'))


#ラック番号表示画面
class RackList(TemplateView):
    model = Rack
    template_name = 'master/rack_list.html'
    
    def post(self, request, *args, **kwargs):
        rack_id = self.request.POST.get('rack_id')
        rack = get_object_or_404(Rack, pk=rack_id)
        rack_number = self.request.POST.get('rack_number')
        rack.rack_number = rack_number
        rack.save()
        return HttpResponseRedirect(reverse('master:rack'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Rack.objects.all()
        return context

class RackAddView(CreateView):
    model = Rack
    fields = ('rack_number',)
    template_name = 'master/rack_add.html'
    success_url = reverse_lazy('master:rack')

class RackShowView(TemplateView):
    model =Rack
    template_name = 'master/rack_show.html'

    def post(self, request, *args, **kwargs):
        rack_id = self.request.POST.get('rack_id')
        rack = Rack.objects.get(pk=rack_id)
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        context['rack'] = rack
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        return context

class RackEditView(TemplateView):
    model = Rack
    fields = ('rack_number')
    template_name = 'master/rack_edit.html'
    success_url = 'rack/'

    def post(self, request, *args, **kwargs):
        rack_id = self.kwargs.get('id')
        rack_number = self.request.POST.get('rack_number')
        rack = get_object_or_404(Rack, pk=rack_id)
        rack.rack_number = rack_number
        rack.save()
        return HttpResponseRedirect(reverse('master:rack'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = RackIdForm()
        context['form'] = RackForm()
        return context

class RackDeleteView(TemplateView):
    model = Rack
    template_name = 'master/rack_delete.html'
        
    def post(self, request, *args, **kwargs):
        rack_id = self.kwargs.get('id')
        rack = get_object_or_404(Rack, pk=rack_id)
        rack.delete()
        return HttpResponseRedirect(reverse('master:rack'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rack_id = self.kwargs.get('id')
        rack = get_object_or_404(Rack, pk=rack_id)
        context['rack'] = rack
        context['form'] = RackIdForm()
        return context
        

#UPS番号表示画面
class UpsList(TemplateView):
    model = Ups 
    template_name = 'master/ups_list.html'
    
    def post(self, request, *args, **kwargs):
        ups_id = self.request.POST.get('ups_id')
        ups = get_object_or_404(Ups, pk=ups_id)
        ups_number = self.request.POST.get('ups_number')
        ups.rack_number = ups_number
        ups.save()
        return HttpResponseRedirect(reverse('master:ups'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Ups.objects.all()
        return context
    
class UpsAddView(CreateView):
    model = Ups
    fields = ('ups_number',)
    template_name = 'master/ups_add.html'
    success_url = reverse_lazy('master:ups')

class UpsShowView(TemplateView):
    model =Ups
    template_name = 'master/ups_show.html'

    def post(self, request, *args, **kwargs):
        ups_id = self.request.POST.get('ups_id')
        ups = Ups.objects.get(pk=ups_id)
        context = super().get_context_data(**kwargs)
        context['form_id'] = UpsIdForm()
        context['ups'] = ups
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UpsIdForm()
        return context

class UpsEditView(TemplateView):
    model = Ups
    fields = ('ups_number')
    template_name = 'master/ups_edit.html'
    success_url = 'ups/'

    def post(self, request, *args, **kwargs):
        ups_id = self.kwargs.get('id')
        ups_number = self.request.POST.get('ups_number')
        ups = get_object_or_404(Ups, pk=ups_id)
        ups.ups_number = ups_number
        ups.save()
        return HttpResponseRedirect(reverse('master:ups'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = UpsIdForm()
        context['form'] = UpsForm()
        return context

class UpsDeleteView(TemplateView):
    model = Ups
    template_name = 'master/ups_delete.html'
        
    def post(self, request, *args, **kwargs):
        ups_id = self.kwargs.get('id')
        ups = get_object_or_404(Ups, pk=ups_id)
        ups.delete()
        return HttpResponseRedirect(reverse('master:ups'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ups_id = self.kwargs.get('id')
        ups = get_object_or_404(Ups, pk=ups_id)
        context['ups'] = ups
        context['form'] = UpsIdForm()
        return context
    

#電源系統表示画面
class PowerSystemList(TemplateView):
    model = PowerSystem
    template_name = 'master/power_system_list.html'
    
    def post(self, request, *args, **kwargs):
        power_system_id = self.request.POST.get('power_system_id')
        power_system = get_object_or_404(PowerSystem, pk=power_system_id)
        power_system_number = self.request.POST.get('power_system_number')
        power_system.poweer_system_number = power_system_number
        max_current = self.request.POST.get('max_current')
        power_system.max_current = max_current
        power_system.save()
        return HttpResponseRedirect(reverse('master:power_system'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = PowerSystem.objects.all()
        return context
    
    
class PowerSystemAddView(CreateView):
    model = PowerSystem
    fields = ('power_system_number', 'max_current', 'supply_source', 'supply_rack')
    template_name = 'master/power_system_add.html'
    success_url = reverse_lazy('master:power_system')
    
class PowerSystemShowView(TemplateView):
    model = PowerSystem
    template_name = 'master/power_system_show.html'

    def post(self, request, *args, **kwargs):
        power_system_id = self.request.POST.get('power_system_id')
        power_system = PowerSystem.objects.get(pk=power_system_id)
        context = super().get_context_data(**kwargs)
        context['form_id'] = PowerSystemIdForm()
        context['power_system'] = power_system
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = PowerSystemIdForm()
        return context

class PowerSystemEditView(TemplateView):#電源系統番号しか変えられない
    model = PowerSystem
    fields = ('power_system_number', 'max_current', 'supply_source', 'supply_rack')
    template_name = 'master/power_system_edit.html'
    success_url = 'power_system/'

    def post(self, request, *args, **kwargs):
        power_system_id = self.kwargs.get('id')
        power_system = get_object_or_404(PowerSystem, pk=power_system_id)
        form = PowerSystemForm(request.POST, instance=power_system)
        form.save()
        return HttpResponseRedirect(reverse('master:power_system'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        power_system_id = self.kwargs.get('id')
        power_system = get_object_or_404(PowerSystem, pk=power_system_id)
        form = PowerSystemForm(instance=power_system)
        context['form_id'] = PowerSystemIdForm()
        context['form'] = form
        return context

class PowerSystemDeleteView(TemplateView):
    model = PowerSystem
    template_name = 'master/power_system_delete.html'
        
    def post(self, request, *args, **kwargs):
        power_system_id = self.kwargs.get('id')
        power_system = get_object_or_404(PowerSystem, pk=power_system_id)
        power_system.delete()
        return HttpResponseRedirect(reverse('master:power_system'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        power_system_id = self.kwargs.get('id')
        power_system = get_object_or_404(PowerSystem, pk=power_system_id)
        context['power_system'] = power_system
        context['form'] = PowerSystemIdForm()
        return context
        