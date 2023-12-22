from django.shortcuts import render

from django.db import models
from datetime import datetime
from apps.measurement.models import CurrentMeasurement
from django.http import HttpResponse
import csv,urllib
# Create your views here.

def csv_export(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    
    date_time = datetime.now() # 日時
    str_time = date_time.strftime('%Y%m%d%H%M')
    
    f = "Current" + "_" + str_time + ".csv"
    filename = urllib.parse.quote((f).encode("utf8"))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response)
    measurement_evaluation_list = CurrentMeasurement.objects.all()
    writer.writerow(['measurement_date', 'current_value', 'power_system', 'employee'])
    for evaluation in measurement_evaluation_list:
        writer.writerow([evaluation.measurement_date, evaluation.current_value, evaluation.power_system.power_system_number, evaluation.employee])
    return response
