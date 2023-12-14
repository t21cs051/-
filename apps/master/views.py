from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Rack, Ups

#ラック番号表示画面
class RackList(TemplateView):
    model = Rack
    template_name = 'master/rack_list.html'
    
    def post(self, request, *args, **kwargs):
        rack_number = self.request.POST.get('rack_number')
        rack = get_object_or_404(Rack, pk=rack_number)
        rack.save()
        return HttpResponseRedirect(reverse('master:rack'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Rack.objects.all()
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
