from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Rack, Ups, PowerSystem
from .forms import RackIdForm, RackForm, PowerSystemForm

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
    fields = ()
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
        ups_number = self.request.POST.get('ups_number')
        ups = get_object_or_404(Rack, pk=ups_number)
        ups.save()
        return HttpResponseRedirect(reverse('master:ups'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Ups.objects.all()
        return context

#電源系統表示画面
class PowerSystemList(TemplateView):
    model = PowerSystem
    template_name = 'master/power_system_list.html'
    
    def post(self, request, *args, **kwargs):
        power_system_number = self.request.POST.get('power_system_number')
        power_system = get_object_or_404(PowerSystem, pk=power_system_number)
        max_current = self.request.POST.get('max_current')
        power_system.max_current = max_current
        power_system.save()
        return HttpResponseRedirect(reverse('master:power_system'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PowerSystemForm()
        return context
    