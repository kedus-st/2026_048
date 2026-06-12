from django.shortcuts import render, redirect
from .models import CalendarEvents, Documents, DPRs

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import json

from backend.blob_actions import save_pdf
import clearance.settings as settings

from django.http import HttpResponse
from django.core.serializers import serialize

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.db.models import Sum
from django.forms.models import model_to_dict
from backend.dprs import generate_dpr_pdf

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return super().default(obj)

@login_required
def calendar(request):

    events = CalendarEvents.objects.all()
    serialized_events = json.dumps(list(events.values()), cls=CustomJSONEncoder, default=str)
    context = {
        'serialized_events': serialized_events,
    }
    return render(request, 'calendar.html', context)

@login_required
def schedule_event(request):
    if('submit') in request.POST:
        if (request.POST.get('eventTitle', False) and request.POST.get('startDateTime', False) and request.POST.get('endDateTime', False) and request.POST.get('eventType', False)):
            event = CalendarEvents()
            if(request.POST.get('eventId', False)):
                event = CalendarEvents.objects.filter(pk=request.POST.get('eventId', False))[0]
            event.title = request.POST.get('eventTitle', False)
            event.start = request.POST.get('startDateTime', False)
            event.end = request.POST.get('endDateTime', False)
            event.type = request.POST.get('eventType', False)
            event.save()
    elif('delete') in request.POST:
        if(request.POST.get('eventId', False)):
            event = CalendarEvents.objects.filter(pk=request.POST.get('eventId', False))[0]
        event.delete()

    events = CalendarEvents.objects.all()
    serialized_events = json.dumps(list(events.values()), cls=CustomJSONEncoder, default=str)
    context = {
        'serialized_events': serialized_events,
    }

    if(request.POST.get('homeCalendar', False)):
        return redirect('index')
    else:
        return redirect('calendar')

@login_required
def documents(request):

    docs = Documents.objects.all()
    serialized_docs = json.dumps(list(docs.values()), cls=CustomJSONEncoder, default=str)
    context = {
        'serialized_docs': serialized_docs,
    }
    return render(request, 'documents.html', context)

@login_required
def doc_upload(request):
    upload = request.FILES['docUpload'].read()
    file_name = request.FILES['docUpload'].name
    file_path = "tmp/"+request.FILES['docUpload'].name
    f = open(file_path, "wb")
    f.write(upload)
    f.close()
    save_pdf(file_path, 'management/docs/'+request.FILES['docUpload'].name)

    doc = Documents()
    doc.file = settings.PROJECT_NAME + '/management/docs/' + file_name
    doc.name = file_name
    doc.uploaded = datetime.now()
    doc.type = request.POST.get('type')

    doc.save()

    return redirect('documents')

@login_required
def weather(request):
    context = {

    }
    return render(request, 'weather.html', context)

def in_seaterra_group(user):
    return user.is_authenticated and user.groups.filter(name="seaterra").exists()

@user_passes_test(in_seaterra_group)
def dprs(request):
    context = {

    }
    return render(request, 'dprs.html', context)

@user_passes_test(in_seaterra_group)
def get_report(request):
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"error": "No date provided. Use ?date=YYYY-MM-DD"}, status=400)

    date_obj = parse_date(date_str)
    if not date_obj:
        return JsonResponse({"error": f"Invalid date '{date_str}'. Expected YYYY-MM-DD."}, status=400)

    dpr = DPRs.objects.filter(date=date_obj).first()

    if not dpr:
        dpr = DPRs.objects.create(date=date_obj)
    data = model_to_dict(dpr)

    data['hse_days_since_start'] = (date_obj - dpr.hse_start).days if dpr.hse_start else ''

    previous = dpr.latest_dpr()
    if previous:
        data['previous_mob_time'] = previous.mob_duration_total
        data['previous_t_time'] = previous.t_duration_total
        data['previous_i_time'] = previous.i_duration_total
        data['previous_cs_time'] = previous.cs_duration_total
        data['previous_wdt_time'] = previous.wdt_duration_total
        data['previous_tbw_time'] = previous.tbw_duration_total
        data['previous_cc_time'] = previous.cc_duration_total
        data['previous_tdt_time'] = previous.tdt_duration_total
        data['previous_total_time'] = previous.total_duration_total

        data['previous_hse_meetings_total'] = previous.hse_meetings_total
        data['previous_hse_toolbox_talks_total'] = previous.hse_toolbox_talks_total
        data['previous_hse_safety_observation_form_total'] = previous.hse_safety_observation_form_total
        data['previous_hse_safety_drills_total'] = previous.hse_safety_drills_total
        data['previous_hse_incidents_total'] = previous.hse_incidents_total
        data['previous_hse_accidents_total'] = previous.hse_accidents_total
        data['previous_hse_working_hours_total'] = previous.hse_working_hours_total
        data['previous_hse_days_without_accident_total'] = previous.hse_days_without_accident_total

        data['previous_mob_duration_total'] = previous.mob_duration_total
        data['previous_t_duration_total'] = previous.t_duration_total
        data['previous_i_duration_total'] = previous.i_duration_total
        data['previous_cs_duration_total'] = previous.cs_duration_total
        data['previous_wdt_duration_total'] = previous.wdt_duration_total
        data['previous_tbw_duration_total'] = previous.tbw_duration_total
        data['previous_cc_duration_total'] = previous.cc_duration_total
        data['previous_tdt_duration_total'] = previous.tdt_duration_total
        data['previous_total_duration_total'] = previous.total_duration_total

    data = JsonResponse(data, safe=False)

    return data

@user_passes_test(in_seaterra_group)
def save_report(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
    data = json.loads(request.body)
    date_str = data.get("date")
    if not date_str:
        return JsonResponse({"error": "No date provided"}, status=400)
    date_obj = parse_date(date_str)
    if not date_obj:
        return JsonResponse({"error": f"Invalid date '{date_str}'. Expected YYYY-MM-DD."}, status=400)
    report = DPRs.objects.filter(date=date_obj).first()
    if not report:
        report = DPRs.objects.create(date=date_obj)

    hse_start_obj = parse_date(data.get("hse_start")) if data.get("hse_start") else None
    report.hse_start = hse_start_obj

    for field, value in data.items():
        if field == "date" or field == "hse_start":
            continue
        if value == "":
            value = None
        if hasattr(report, field):
            setattr(report, field, value)

    report.save()

    return JsonResponse({"status": "success"})

@user_passes_test(in_seaterra_group)
def reload_totals(request):
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"error": "No date provided. Use ?date=YYYY-MM-DD"}, status=400)

    date_obj = parse_date(date_str)
    if not date_obj:
        return JsonResponse({"error": f"Invalid date '{date_str}'. Expected YYYY-MM-DD."}, status=400)

    dpr = DPRs.objects.filter(date=date_obj).first()
    if not dpr:
        return JsonResponse({"error": f"No DPR found for date '{date_str}'."}, status=404)
    dpr.load_totals()
    dpr.save()

    return JsonResponse({"status": "success"})

@user_passes_test(in_seaterra_group)
def reset_dprs(request):
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"error": "No date provided. Use ?date=YYYY-MM-DD"}, status=400)

    date_obj = parse_date(date_str)
    if not date_obj:
        return JsonResponse({"error": f"Invalid date '{date_str}'. Expected YYYY-MM-DD."}, status=400)

    dpr = DPRs.objects.filter(date=date_obj).first()

    if not dpr:
        return JsonResponse({"error": f"No DPR found for date '{date_str}'."}, status=404)
    
    dpr.delete()

    return JsonResponse({"status": "success"})

@user_passes_test(in_seaterra_group)
def print_dpr(request):
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"error": "No date provided. Use ?date=YYYY-MM-DD"}, status=400)

    date_obj = parse_date(date_str)
    if not date_obj:
        return JsonResponse({"error": f"Invalid date '{date_str}'. Expected YYYY-MM-DD."}, status=400)

    dpr = DPRs.objects.filter(date=date_obj).first()
    if not dpr:
        return JsonResponse({"error": f"No DPR found for date '{date_str}'."}, status=404)

    response = generate_dpr_pdf(dpr.date)
    response['Content-Disposition'] = f'inline; filename="DPR_{date_str}.pdf"'
    return response

@user_passes_test(in_seaterra_group)
def copy_dpr(request):
    source_date = request.GET.get("sourceDate")
    target_date = request.GET.get("targetDate")
    if not source_date or not target_date:
        return JsonResponse({"error": "Both sourceDate and targetDate must be provided"}, status=400)
    
    source_date_obj = parse_date(source_date)
    target_date_obj = parse_date(target_date)
    if not source_date_obj or not target_date_obj:
        return JsonResponse({"error": "Invalid date format. Expected YYYY-MM-DD."}, status=400)
    
    source_dpr = DPRs.objects.filter(date=source_date_obj).first()
    if not source_dpr:
        return JsonResponse({"error": f"No DPR found for source date '{source_date}'."}, status=404)
    target_dpr = DPRs.objects.filter(date=target_date_obj).first()
    copyable_fields = [
        'ceo',
        'project_manager',
        'ocm',
        'eod_manager',
        'captain',
        'client_rep',
        'vessel_email',
        'distribution_list',
        'marine_onsigners',
        'seaterra_onsigners',
        'client_onsigners',
        'marine_offsigners',
        'seaterra_offsigners',
        'client_offsigners',
        'routine_vessel',
        'routine_total_targets',
        'hse_meetings_total',
        'hse_toolbox_talks_total',
        'hse_safety_observation_form_total',
        'hse_safety_drills_total',
        'hse_incidents_total',
        'hse_accidents_total',
        'hse_working_hours_total',
        'hse_days_without_accident_total',      
    ]
    for field in copyable_fields:
        setattr(target_dpr, field, getattr(source_dpr, field))
    target_dpr.save()

    return JsonResponse({"status": "success"})

@user_passes_test(in_seaterra_group)
def dpr_statistics(request):
    return render(request, 'dpr_statistics.html')