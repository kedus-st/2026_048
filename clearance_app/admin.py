from django.contrib import admin

from import_export.admin import ImportExportMixin, ImportExportActionModelAdmin
from import_export.formats import base_formats
from leaflet.admin import LeafletGeoAdminMixin
from reversion.admin import VersionAdmin

from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter

from .models import MtlItem, MtlItemImage, Documents, UnlinkedImage, Vessel

from .resources import MtlItemResource

from clearance import settings

from .forms import UnlinkedImageForm, UploadFilesForm

from django.utils.html import format_html

from backend.trs2 import create_tr
from backend.container_receipts import create_hoc_receipt, create_wsc_receipt

from django.utils.translation import gettext_lazy as _

from admin_auto_filters.filters import AutocompleteFilter

import csv
from django.http import HttpResponse

SRID = settings.EPSG

class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 1
    STEP = 1

    def queryset(self, request, queryset):
        param_from = f'{self.parameter_name}_from'
        param_to = f'{self.parameter_name}_to'

        raw_min = request.GET.get(param_from)
        raw_max = request.GET.get(param_to)

        try:
            min_val = round(float(raw_min), self.MAX_DECIMALS) if raw_min else None
            max_val = round(float(raw_max), self.MAX_DECIMALS) if raw_max else None

            filter_kwargs = {}
            if min_val is not None:
                filter_kwargs[f'{self.field_path}__gte'] = min_val
            if max_val is not None:
                filter_kwargs[f'{self.field_path}__lte'] = max_val

            return queryset.filter(**filter_kwargs)
        except (TypeError, ValueError):
            return queryset


class CustomRangeNumericFilter(RangeNumericFilter):
    MAX_DECIMALS = 1
    STEP = 1

    def queryset(self, request, queryset):
        param_from = f'{self.parameter_name}_from'
        param_to = f'{self.parameter_name}_to'

        raw_min = request.GET.get(param_from)
        raw_max = request.GET.get(param_to)

        try:
            min_val = round(float(raw_min), self.MAX_DECIMALS) if raw_min else None
            max_val = round(float(raw_max), self.MAX_DECIMALS) if raw_max else None

            filter_kwargs = {}
            if min_val is not None:
                filter_kwargs[f'{self.field_path}__gte'] = min_val
            if max_val is not None:
                filter_kwargs[f'{self.field_path}__lte'] = max_val

            return queryset.filter(**filter_kwargs)
        except (TypeError, ValueError):
            return queryset


class MtlItemImageInline(admin.TabularInline):
    model = MtlItemImage


@admin.register(MtlItem)
class MtlItemAdmin(LeafletGeoAdminMixin, ImportExportMixin, VersionAdmin, ImportExportActionModelAdmin,
                   NumericFilterModelAdmin):
    '''
    def has_import_permission(self, request):
        if request.user.groups.filter(name='seaterra').exists():
            return True
        return False
    
    def has_export_permission(self, request):
        if request.user.groups.filter(name='seaterra').exists():
            return True
        return False
    '''
    
    change_form_template = "admin/mtlitem_change_form.html"

    def debug(modeladmin, request, queryset):
        count = 0
        targets_in_safety_zone = [
            'ITP-0735', 'ITP-0754', 'ITP-0756', 'ITP-0764', 'ITP-0759', 'ITP-0752', 'ITP-0739',
            'ITP-0782', 'ITP-0742', 'ITP-0748', 'ITP-0770', 'ITP-0798', 'ITP-0825', 'ITP-0818',
            'ITP-0803', 'ITP-0848', 'ITP-0853'
        ]
        targets_in_client_list = [
            'ITP-0806', 'ITP-0783', 'ITP-0824', 'ITP-0822', 'ITP-0821', 'ITP-0801', 'ITP-0800',
            'ITP-0799', 'ITP-0833', 'ITP-0834', 'ITP-0840', 'ITP-0841', 'ITP-0842'
        ]
        for target in targets_in_client_list:
            try:
                mtl_item = MtlItem.objects.get(itp_no_mag=target)
                mtl_item.todo_target = ''
                mtl_item.tr_comment = 'Auf Kundenwunsch nicht geräumt'
                mtl_item.save()
                count += 1
                print("Target updated:", target)
            except:
                print("Target not found:", target)
        print("Total updated:", count)

    def recreate_target_records(modeladmin, request, queryset):
        for mtl_item in queryset:
            create_tr(mtl_item)

    def export_for_ags(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=targetlist_for_ags.csv'

        writer = csv.writer(response)
        #writer.writerow(["Punktnummer", "Easting", "Northing", "Done", "Recheck"])

        for item in queryset:
            done = 1 if item.clear == 'y' else 0
            recheck = 1 if item.clear == 'w' else 0
            writer.writerow([item.itp_no_mag, item.easting, item.northing, done, recheck])

        return response

    def recalculate_geom(modeladmin, request, queryset):
        for item in queryset:
            print("Calculating geometry")
            item.geom = item.get_geom()
            print("Geometry calculated:", item.geom)
            item.save()
        #geometry = GEOSGeometry('POINT(%s %s)' % (modeladmin.fields['easting'], modeladmin.fields['northing']), srid=SRID)
        #return geometry

    recreate_target_records.short_description = 'Recreate Target Records'
    export_for_ags.short_description = 'Export Selected Items for AGS Track'
    debug.short_description = 'Debug - For Debug Use Only!'
    recalculate_geom.short_description = 'Recalculate Geometry'


    resource_class = MtlItemResource
    list_display = ('itp_no_mag',
                    # 'easting_2',
                    # 'northing_2',
                    'easting',
                    'northing',
                    # 'model_depth_below_ground',
                    # 'model_weight',
                    # 'mag_moment',
                    # 'anomaly_max',
                    # 'anomaly_min',
                    # 'dipole_pp',
                    # 'tfem_mag_moment',
                    # 'tfem_anomaly_max',
                    # 'tfem_anomaly_min',
                    # 'tfem_dipole_width',
                    # 'tfem_dipole_pp',
                    # 'munition_category',
                    'todo_target',
                    'cl_date',
                    'cl_time',
                    'uxo',
                    'model_weight',
                    'clear',
                    'qa_clear',
                    'description_detail',
                    'tr_comment',
                    'eod',
                    'surveyor',
                    'updated',
                    'created')
    list_editable = ('todo_target',
                     'cl_date',
                     'cl_time',
                     'uxo',
                     'clear',
                     'qa_clear',
                     'description_detail',
                     'eod',
                     'surveyor')
    list_filter = (
        'clear',
        'uxo',
        'todo_target',
        'prio',
        'section',
        ('model_weight', CustomSliderNumericFilter),
        ('model_weight', CustomRangeNumericFilter),
        ('mag_moment', CustomRangeNumericFilter),
        'todo_target',
        'eod',
        'surveyor',
        'munition_category',
        'cl_date',
        #'cl_time',
        'created',
        ('easting', CustomSliderNumericFilter),
        ('northing', CustomSliderNumericFilter),
        ('water_depth_geoid', CustomSliderNumericFilter),
        ('model_depth_geoid', CustomSliderNumericFilter),
        ('anomaly_max', CustomSliderNumericFilter),
        ('anomaly_min', CustomSliderNumericFilter),
        ('dipole_width', CustomSliderNumericFilter),
        ('dipole_pp', CustomSliderNumericFilter),


    )
    # readonly_fields = ('created', 'updated')
    inlines = [MtlItemImageInline]
    search_fields = ['itp_no_mag', 'description_detail', 'eod']
    ordering = ('itp_no_mag',)
    actions = [
        recreate_target_records,
        export_for_ags,
        #debug,
        #recalculate_geom
    ]
    list_per_page = 30
    save_on_top = True

    def get_export_formats(self):
        formats = (base_formats.CSV, base_formats.XLSX,)
        return [f for f in formats if f().can_export()]
    
    #def get_list_display(self, request):
    #    self.list_display = self.list_display
    #    return self.list_display
    # def get_import_formats(self):
    #     formats = (base_formats.CSV, base_formats.XLSX,)
    #     return [f for f in formats if f().can_import()]
    def get_model_fields(self):
        fields_to_skip = ['id', 'itp_no_mag', 'mtlimage',]
        return [(field.name, field.verbose_name) for field in MtlItem._meta.get_fields() if field.name not in fields_to_skip]
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['mtlitem'] = self.get_object(request, object_id)
        return super(MtlItemAdmin, self).change_view(request, object_id, form_url, extra_context)

class UnlinkedImageAdmin(admin.ModelAdmin):
    form = UnlinkedImageForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        # Ensure that form.save() is called to handle multiple images
        if 'images' in request.FILES:
            #print(obj)
            form.save(commit=True)
        else:
            super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Prevent the save_m2m issue
        if hasattr(form, 'save_m2m'):
            form.save_m2m()
        super().save_related(request, form, formsets, change)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))
        return "No Image"
    
    image_tag.short_description = 'Image'

    def image_link(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.image.url, obj.image.url)
    image_link.short_description = 'Image Link'

    list_display = ['image_tag', 'image_link', 'notes']

admin.site.register(UnlinkedImage, UnlinkedImageAdmin)

admin.site.register(MtlItemImage)

admin.site.register(Documents)

admin.site.register(Vessel)