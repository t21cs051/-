from django.shortcuts import render
from django.db import models
from datetime import datetime
from apps.measurement.models import CurrentMeasurement
from apps.worklog.models import WorkLog
from apps.master.models import Ups, Rack, PowerSystem
from django.http import HttpResponse
import csv,urllib

def measurement_export(request):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    
    date_time = datetime.now() # 日時
    str_time = date_time.strftime('%Y%m%d%H%M')
    
    f = "Current" + "_" + str_time + ".csv"
    filename = urllib.parse.quote((f).encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response)
    measurement_evaluation_list = CurrentMeasurement.objects.all()
    writer.writerow(['date', 'current_value', 'power_system', 'employee'])
    for evaluation in measurement_evaluation_list:
        writer.writerow([evaluation.date, evaluation.current_value, evaluation.power_system.power_system_number, evaluation.employee])
    return response


def worklog_export(request):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    
    date_time = datetime.now() # 日時
    str_time = date_time.strftime('%Y%m%d%H%M')
    
    f = "WorkLog" + "_" + str_time + ".csv"
    filename = urllib.parse.quote((f).encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response)
    worklog_list = WorkLog.objects.all()
    writer.writerow(['date', 'rack', 'work_type', 'description', 'employee'])
    for worklog in worklog_list:
        writer.writerow([worklog.date, worklog.rack.rack_number, worklog.get_work_type_display(), worklog.description, worklog.employee])
    return response

def ups_export(request):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    
    date_time = datetime.now() # 日時
    str_time = date_time.strftime('%Y%m%d%H%M')
    
    f = "Ups" + "_" + str_time + ".csv"
    filename = urllib.parse.quote((f).encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response)
    ups_list = Ups.objects.all()
    writer.writerow(['ups_number', 'description'])
    for ups in ups_list:
        writer.writerow([ups.ups_number, ups.description])
    return response

def rack_export(request):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    
    date_time = datetime.now() # 日時
    str_time = date_time.strftime('%Y%m%d%H%M')
    
    f = "Rack" + "_" + str_time + ".csv"
    filename = urllib.parse.quote((f).encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response)
    rack_list = Rack.objects.all()
    writer.writerow(['rack_number', 'description'])
    for rack in rack_list:
        writer.writerow([rack.rack_number, rack.description])
    return response

def powersystem_export(request):
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    
    date_time = datetime.now() # 日時
    str_time = date_time.strftime('%Y%m%d%H%M')
    
    f = "PowerSystem" + "_" + str_time + ".csv"
    filename = urllib.parse.quote((f).encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response)
    power_system_list = PowerSystem.objects.all()
    writer.writerow(['power_system_number', 'max_current', 'supply_source', 'supply_rack'])
    for power_system in power_system_list:
        writer.writerow([power_system.power_system_number, power_system.max_current, power_system.supply_source.ups_number, power_system.supply_rack.rack_number])
    return response