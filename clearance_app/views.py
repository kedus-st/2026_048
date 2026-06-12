from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required, user_passes_test

from .models import MtlItem, UnlinkedImage, MtlItemImage, Vessel

from django.core.serializers import serialize

from backend.blob_actions import list_blob_data, get_secure_blob_url

from backend.blob_actions import save_img

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .admin import MtlItemAdmin

from django.http import HttpResponseRedirect

from management.models import CalendarEvents
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import json, requests

from django.db.models import Count, Sum

from management.models import OperationalHours

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt

from clearance.settings import EPSG, VESSELFINDER_API_KEY

from django.db.models import OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from pyproj import Proj, transform

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return super().default(obj)
    
def group_required(group_names):
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) or user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@login_required
def index(request):

    mtl_items_count = MtlItem.objects.count()
    
    if mtl_items_count is not None:
        mtl_items_to_clear_count = MtlItem.objects.filter(todo_target__exact='x').count()
        mtl_items_to_clear_count_percent = round(
            (mtl_items_to_clear_count / (mtl_items_count / 100) if mtl_items_count else 0), 1)
        mtl_items_clear_count = MtlItem.objects.filter(clear__exact='y').count()
        mtl_items_waiting_count = MtlItem.objects.filter(clear__exact='w').count()
        mtl_items_not_clear_count = MtlItem.objects.filter(todo_target__exact='x').exclude(clear__exact='y').exclude(clear__exact='w').count()
        mtl_items_not_checked_count = mtl_items_count - mtl_items_clear_count - mtl_items_waiting_count - mtl_items_not_clear_count
        mtl_items_open_count = mtl_items_waiting_count
        mtl_items_uxo_count = MtlItem.objects.filter(uxo__exact='x').count()
        mtl_items_sentinel = MtlItem.objects.filter(vessel__exact='RS Sentinel', clear__exact='y').count()
        mtl_items_kamara = MtlItem.objects.filter(vessel__exact='Kamara', clear__exact='y').count()
        
        if mtl_items_to_clear_count > 0:
            mtl_items_clear_count_percent = round(
                (mtl_items_clear_count / (mtl_items_to_clear_count / 100) if mtl_items_count else 0), 1)
            mtl_items_waiting_count_percent = round(
                (mtl_items_waiting_count / (mtl_items_to_clear_count / 100) if mtl_items_count else 0), 1)
            mtl_items_not_clear_count_percent = round(
                (mtl_items_not_clear_count / (mtl_items_to_clear_count / 100) if mtl_items_not_clear_count else 0), 1)
            mtl_items_not_checked_count_percent = round(
                (mtl_items_not_checked_count / (mtl_items_to_clear_count / 100) if mtl_items_not_checked_count else 0), 1)
            mtl_items_open_count_percent = round(
                (mtl_items_open_count / (mtl_items_to_clear_count / 100) if mtl_items_not_checked_count else 0), 1)
            mtl_items_uxo_count_percent = round(
                (mtl_items_uxo_count / (mtl_items_to_clear_count / 100) if mtl_items_uxo_count else 0), 1)
        else:
            mtl_items_clear_count_percent = 0
            mtl_items_waiting_count_percent = 0
            mtl_items_not_clear_count_percent = 0
            mtl_items_not_checked_count_percent = 0
            mtl_items_open_count_percent = 0
            mtl_items_uxo_count_percent = 0


        events = CalendarEvents.objects.all()
        serialized_events = json.dumps(list(events.values()), cls=CustomJSONEncoder, default=str)

        clearance_dates_wh = MtlItem.objects.all().exclude(cl_date__isnull=True) \
            .filter(clear__exact = 'y') \
            .values('cl_date') \
            .annotate(count=Count('cl_date')) \
            .order_by('cl_date')
        
        operational_hours = OperationalHours.objects.values('date') \
        .annotate(total_hours=Sum('hours')) 

        operational_hours_dict = {entry['date']: entry['total_hours'] for entry in operational_hours}

        clearance_dates = [
        {
            'cl_date': entry['cl_date'],
            'count': entry['count'],
            'hours': operational_hours_dict.get(entry['cl_date'], 0)
        }
            for entry in clearance_dates_wh
        ]


        mtlitems = MtlItem.objects.all()
        serialized_mtlitems = serialize('json', mtlitems)

        vessels = Vessel.objects.all()

        context = {

            # Counts
            'mtl_items_count': mtl_items_count,
            'mtl_items_uxo_count': mtl_items_uxo_count,
            'mtl_items_uxo_count_percent': mtl_items_uxo_count_percent,
            'mtl_items_clear_count': mtl_items_clear_count,
            'mtl_items_clear_count_percent': mtl_items_clear_count_percent,
            'mtl_items_to_clear_count': mtl_items_to_clear_count,
            'mtl_items_to_clear_count_percent': mtl_items_to_clear_count_percent,
            'mtl_items_waiting_count': mtl_items_waiting_count,
            'mtl_items_waiting_count_percent': mtl_items_waiting_count_percent,
            'mtl_items_not_clear_count': mtl_items_not_clear_count,
            'mtl_items_not_clear_count_percent': mtl_items_not_clear_count_percent,
            'mtl_items_open_count': mtl_items_open_count,
            'mtl_items_open_count_percent': mtl_items_open_count_percent,
            'mtl_items_not_checked_count': mtl_items_not_checked_count,
            'mtl_items_not_checked_count_percent': mtl_items_not_checked_count_percent,
            'mtl_items_sentinel': mtl_items_sentinel,
            'mtl_items_kamara': mtl_items_kamara,

            'serialized_events': serialized_events,

            'clearance_dates': list(clearance_dates),

            'mtlitems': mtlitems,
            'serialized_mtlitems': serialized_mtlitems,
            'vessels': vessels,

        }
    return render(request, 'home.html', context)


@login_required
def mtl_items_view(request):
    mtl_items = serialize('geojson', MtlItem.objects.all())
    return HttpResponse(mtl_items, content_type='geojson')

@login_required
def vessel_items_view(request):
    vessel_items = serialize('geojson', Vessel.objects.all())
    return HttpResponse(vessel_items, content_type='geojson')

class Img():
    link = ''
    date = ''
    name = ''

@login_required
def picture_gallery(request):
    pictures = []
    imgs = list_blob_data('media/mtlimages')
    for img in imgs:
        image = Img()
        image.link = get_secure_blob_url(img.name)
        image.name =  img.name.rsplit('/', 1)[-1]
        image.date = img.creation_time
        pictures.append(image)
    
    pictures = pictures[1:]

    items_per_page = request.GET.get('items_per_page', 24)
    paginator = Paginator(pictures, items_per_page)
    page = request.GET.get('page', 1)


    try:
        pictures = paginator.page(page)
    except PageNotAnInteger:
        pictures = paginator.page(1)
    except EmptyPage:
        pictures = paginator.page(paginator.num_pages)

    context = {
        'pictures': pictures,

    }
    return render(request, 'picture_gallery.html', context)


class TR():
    link = ''
    name = ''

@login_required
def tr_view(request):
    records = list_blob_data('media/targetrecords')
    trs = []
    for record in records:
        tr = TR()
        tr.link = get_secure_blob_url(record.name)
        tr.name =  record.name.rsplit('/', 1)[-1]
        trs.append(tr)

    trs = trs[1:]

    context = {
        'trs': trs,
    }

    return render(request, 'tr_view.html', context)


@login_required
@group_required(['seaterra',])
def itp_edit(request):

    if request.POST.get('itp_no_mag', False):
        mtl = MtlItem.objects.filter(itp_no_mag=request.POST.get('itp_no_mag', False))[0]
        if request.POST.get('found-dropdown', False):
            mtl.found = request.POST.get('found-dropdown', False)
        if request.POST.get('recovered-dropdown', False):
            mtl.salvaged = request.POST.get('recovered-dropdown', False)
        if request.POST.get('uxo-dropdown', False):
            mtl.uxo = request.POST.get('uxo-dropdown', False)
        if request.POST.get('clear-dropdown', False):
            mtl.clear = request.POST.get('clear-dropdown', False)
        if request.POST.get('qa-clear-dropdown', False):
            mtl.qa_clear = request.POST.get('qa-clear-dropdown', False)
        if request.POST.get('todo-dropdown', False):
            mtl.todo_target = request.POST.get('todo-dropdown', False)
        
        if request.POST.get('weight', False):
            mtl.cl_weight = request.POST.get('weight', False)
        if request.POST.get('width', False):
            mtl.cl_width = request.POST.get('width', False)
        if request.POST.get('length', False):
            mtl.cl_length = request.POST.get('length', False)
        
        if request.POST.get('tr-comment', False):
            mtl.tr_comment = request.POST.get('tr-comment', False)
        if request.POST.get('description-detail', False):
            mtl.description_detail = request.POST.get('description-detail', False)
        
        if 'imageUpload' in request.FILES:
            for file in request.FILES.getlist('imageUpload'):

                image_count = MtlItemImage.objects.filter(mtl_item=mtl).count() + 1

                file_extension = file.name.split('.')[-1]
                new_filename = f"{mtl.itp_no_mag}_pic_{image_count}.{file_extension}"

                mtl_image = MtlItemImage(mtl_item=mtl)
                upload_path = mtl_image.upload_to(new_filename)

                saved_filename = default_storage.save(upload_path, ContentFile(file.read()))
                
                mtl_image.mtl_item_image = saved_filename
                mtl_image.save()
            
            '''
            upload = request.FILES['imageUpload'].read()
            file_path = "tmp/"+request.FILES['imageUpload'].name
            f = open(file_path, "wb")
            f.write(upload)
            f.close()

            mtl_image = MtlItemImage(mtl_item=obj)
            upload_path = mtl_image.upload_to(new_filename)

            # Save the file using the custom path
            saved_filename = default_storage.save(upload_path, ContentFile(file.read()))
            
            # Create a new MtlItemImage record
            mtl_image.mtl_item_image = saved_filename
            mtl_image.save()

            save_img(file_path, 'media/mtlimages/'+request.FILES['imageUpload'].name)
            '''


        mtl.save()
    
    mtl_items_count = MtlItem.objects.count()
    
    if mtl_items_count is not None:
        mtl_items_to_clear_count = MtlItem.objects.filter(todo_target__exact='x').count()
        mtl_items_to_clear_count_percent = round(
            (mtl_items_to_clear_count / (mtl_items_count / 100) if mtl_items_count else 0), 1)
        
        mtl_items_clear_count = MtlItem.objects.filter(clear__exact='y').count()
        mtl_items_waiting_count = MtlItem.objects.filter(clear__exact='w').count()
        mtl_items_not_clear_count = MtlItem.objects.filter(todo_target__exact='x').exclude(clear__exact='y').exclude(clear__exact='w').count()
        mtl_items_not_checked_count = mtl_items_count - mtl_items_clear_count - mtl_items_waiting_count - mtl_items_not_clear_count
        mtl_items_open_count = mtl_items_waiting_count
        mtl_items_uxo_count = MtlItem.objects.filter(uxo__exact='x').count()
        mtl_items_sentinel = MtlItem.objects.filter(vessel__exact='RS Sentinel', clear__exact='y').count()
        mtl_items_kamara = MtlItem.objects.filter(vessel__exact='Kamara', clear__exact='y').count()

        
        if mtl_items_to_clear_count > 0:
            mtl_items_clear_count_percent = round(
                (mtl_items_clear_count / (mtl_items_to_clear_count / 100) if mtl_items_count else 0), 1)
            mtl_items_waiting_count_percent = round(
                (mtl_items_waiting_count / (mtl_items_to_clear_count / 100) if mtl_items_count else 0), 1)
            mtl_items_not_clear_count_percent = round(
                (mtl_items_not_clear_count / (mtl_items_to_clear_count / 100) if mtl_items_not_clear_count else 0), 1)
            mtl_items_not_checked_count_percent = round(
                (mtl_items_not_checked_count / (mtl_items_to_clear_count / 100) if mtl_items_not_checked_count else 0), 1)
            mtl_items_open_count_percent = round(
                (mtl_items_open_count / (mtl_items_to_clear_count / 100) if mtl_items_not_checked_count else 0), 1)
            mtl_items_uxo_count_percent = round(
                (mtl_items_uxo_count / (mtl_items_to_clear_count / 100) if mtl_items_uxo_count else 0), 1)
        else:
            mtl_items_clear_count_percent = 0
            mtl_items_waiting_count_percent = 0
            mtl_items_not_clear_count_percent = 0
            mtl_items_not_checked_count_percent = 0
            mtl_items_open_count_percent = 0
            mtl_items_uxo_count_percent = 0

        vessels = Vessel.objects.all()

        context = {

            # Counts
            'mtl_items_count': mtl_items_count,
            'mtl_items_uxo_count': mtl_items_uxo_count,
            'mtl_items_uxo_count_percent': mtl_items_uxo_count_percent,
            'mtl_items_clear_count': mtl_items_clear_count,
            'mtl_items_clear_count_percent': mtl_items_clear_count_percent,
            'mtl_items_to_clear_count': mtl_items_to_clear_count,
            'mtl_items_to_clear_count_percent': mtl_items_to_clear_count_percent,
            'mtl_items_waiting_count': mtl_items_waiting_count,
            'mtl_items_waiting_count_percent': mtl_items_waiting_count_percent,
            'mtl_items_not_clear_count': mtl_items_not_clear_count,
            'mtl_items_not_clear_count_percent': mtl_items_not_clear_count_percent,
            'mtl_items_open_count': mtl_items_open_count,
            'mtl_items_open_count_percent': mtl_items_open_count_percent,
            'mtl_items_not_checked_count': mtl_items_not_checked_count,
            'mtl_items_not_checked_count_percent': mtl_items_not_checked_count_percent,
            'mtl_items_sentinel': mtl_items_sentinel,
            'mtl_items_kamara': mtl_items_kamara,
            
            'vessels': vessels,

        }
    return render(request, 'home.html', context)

def visible_mtl_cols(request):
    modeladmin = MtlItemAdmin
    model = MtlItem
    displayed_cols = ['itp_no_mag']

    all_cols = model._meta.get_fields()
    selected_cols = []
    for col in all_cols:
        if(request.POST.get(col.name, False)):
            if(col.name == 'itp_no_mag'):
                pass
            else:
                displayed_cols.append(col.name)
            selected_cols.append(col.name)
    modeladmin.list_display = displayed_cols
    request.session['selected_cols'] = selected_cols
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def statistics(request):
    return render(request, 'statistics.html')

@login_required
def get_sas_token_view(request):
    blob_name = request.GET.get('blob_name')
    
    if not blob_name:
        return JsonResponse({'error': 'Blob name is required'}, status=400)

    url = get_secure_blob_url(blob_name)
    
    return JsonResponse({'url': url})

@login_required
def get_image_sources(request):
    itp_no_mag = request.GET.get('itp_no_mag')

    if not itp_no_mag:
        return JsonResponse({'error': 'ITP No MAG is required'}, status=400)

    images = MtlItemImage.objects.filter(mtl_item__itp_no_mag=itp_no_mag)
    image_sources = []
    for image in images:
        image_sources.append(image.mtl_item_image.url)
    if len(image_sources) == 0:
        image_sources.append('/static/img/no_img.jpg')

    return JsonResponse({'image_sources': image_sources})

@login_required
def update_vessel_position(request, vessel_id):
    try:
        vessel = get_object_or_404(Vessel, id=vessel_id)

        api_key = VESSELFINDER_API_KEY
        base_url = "https://api.vesselfinder.com/vessels"
        params = {
            'userkey': api_key,
            'mmsi': vessel.mmsi
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if len(data) > 0 and 'AIS' in data[0]:
            vessel_info = data[0]['AIS']
            
            latitude = vessel_info.get('LATITUDE')
            longitude = vessel_info.get('LONGITUDE')
            
            if latitude is not None and longitude is not None:
                proj = Proj(f"EPSG:{EPSG}")
                
                easting, northing = proj(longitude, latitude)
                
                vessel.easting = easting
                vessel.northing = northing

                
                vessel.save()
            else:
                raise ValueError("No position data found for the requested vessel.")
        else:
            raise ValueError("No vessel data found for the provided MMSI.")

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")