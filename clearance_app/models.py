from django.contrib.gis.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.point import Point
from django.utils import timezone
from django.db.models import Sum

from backend.custom_azure import AzureMediaStorage as AMS
from backend.blob_actions import save_pdf
from backend.blob_actions import list_blobs, overwrite_tr, delete_img, overwrite_duplicate, upload_xyz, delete_file


from clearance import settings

import os, datetime, math

from django.core.files.storage import FileSystemStorage

from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.utils.safestring import mark_safe

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

SRID = settings.EPSG

X_CHOICES = [
    ('', ''),
    ('x', 'x'),
]

TODO_CHOICES = [
    ('', ''),
    ('x', 'x'),
    ('f', 'f'),
    ('n', 'n')
]

YES_NO_CHOICES = [
    ('', ''),
    ('y', _('JA')),
    ('n', _('NEIN')),
]

YES_NO_STRICKT_CHOICES = [
    ('y', _('JA')),
    ('n', _('NEIN')),
]

YES_NO_WAITING_CHOICES = [
    ('', ''),
    ('y', _('JA')),
    ('n', _('NEIN')),
    ('w', _('IN ARBEIT')),
]


class MtlItem(models.Model):
    itp_no_mag = models.CharField(max_length=50, verbose_name='ITP No. MAG', unique=True)
    # itp_no_sss = models.CharField(verbose_name='ITP No. SSS', max_length=30, blank=True, null=True)

    # Survery Info
    easting = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Easting')
    northing = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Northing')
    lat = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Breitengrad'))
    lon = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Längengrad'))
    water_depth_geoid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                            verbose_name=_('Wassertiefe [m]'))
    model_depth_geoid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                            verbose_name=_('Modelltiefe [m]'))
    model_depth_below_ground = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                                   verbose_name=_('Modelltiefe unter GOK [m]'))
    model_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       verbose_name=_('Modelgewicht [kg]'))
    mag_moment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                     verbose_name=_('MAG Moment [A/m²]'))
    anomaly_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      verbose_name=_('Anomaly max [nT]'))
    anomaly_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      verbose_name=_('Anomaly min [nT]'))
    dipole_width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                       verbose_name=_('Dipole Breite [m]'))
    dipole_pp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                    verbose_name=_('Dipole P-P [nT]'))
    itp_notes = models.CharField(verbose_name=_('ITP Notizen'), max_length=200, blank=True, null=True)

    # Clearance Info
    munition_category = models.CharField(
        verbose_name='Mun. cat.',
        max_length=250,
        blank=True, null=True,
        # choices=MUNITION_CATEGORY_CHOICES
    )
    todo_target = models.CharField(max_length=1, blank=True, null=True, choices=TODO_CHOICES, verbose_name=_('todo_target'))
    prio = models.IntegerField(null=True, blank=True, verbose_name=_('Priorität'))  # added 10.05.2022
    section = models.CharField(max_length=3, null=True, blank=True, verbose_name=_('Sektion'))
    cl_date = models.DateField(verbose_name=_('Bergungsdatum'), blank=True, null=True)
    cl_time = models.TimeField(verbose_name=_('Bergungszeit'), blank=True, null=True)
    vessel = models.CharField(verbose_name=_('Schiff'), max_length=30, blank=True, null=True)
    eod = models.CharField(verbose_name=_('Feuerwerker'), max_length=50, blank=True, null=True)
    surveyor = models.CharField(verbose_name=_('Vermesser'), max_length=50, blank=True, null=True)
    clearance_co = models.CharField(verbose_name=_('Räumfirma'), max_length=50, blank=True, null=True)

    # Clearance Results
    cl_weight = models.DecimalField(verbose_name=_('Gewicht (kg)'), max_digits=10, decimal_places=2, blank=True, null=True)
    cl_length = models.DecimalField(verbose_name=_('Länge (m)'), max_digits=10, decimal_places=2, blank=True, null=True)
    cl_width = models.DecimalField(verbose_name=_('Breite (m)'), max_digits=10, decimal_places=2, blank=True, null=True)
    cl_depth_bg = models.DecimalField(verbose_name=_('Tiefe GOK (m)'), max_digits=10, decimal_places=2, blank=True,
                                      null=True)
    tr_comment = models.TextField(verbose_name=_('TR Kommentar'), max_length=500, blank=True, null=True)
    found = models.CharField(verbose_name=_('gefunden (y/n)'), max_length=1, blank=True, null=True, choices=YES_NO_CHOICES)
    salvaged = models.CharField(verbose_name=_('geborgen (y/n/w)'), max_length=1, blank=True, null=True,
                                choices=YES_NO_WAITING_CHOICES)
    uxo = models.CharField(verbose_name=_('Kampfmittel (x)'), max_length=1, blank=True, null=True, choices=X_CHOICES)

    to_detonate = models.CharField(verbose_name=_('zu sprengen (y/n)'), max_length=1, blank=True, null=True, choices=YES_NO_CHOICES)
    detonated = models.CharField(verbose_name=_('gesprengt (y/n/w)'), max_length=1, blank=True, null=True, choices=YES_NO_WAITING_CHOICES)
    safety_dist = models.DecimalField(verbose_name=_('Sicherheitsabstand (m)'), max_digits=10, decimal_places=2, blank=True, null=True)

    # Clearance Status
    clear = models.CharField(verbose_name=_('frei (y/n/w)'), max_length=1, null=True, blank=True,
                             choices=YES_NO_WAITING_CHOICES)
    # qa_responsible = models.CharField(verbose_name='QA Prüfer', max_length=100, null=True, blank=True)
    qa_clear = models.CharField(verbose_name=_('QA Freigabe (y)'), max_length=1, default='n',
                                choices=YES_NO_STRICKT_CHOICES,
                                null=True, blank=True)
    description_detail = models.CharField(verbose_name=_('Beschreibung'), max_length=300, blank=True, null=True)
    qa_comments = models.CharField(verbose_name=_('QA Kommentare'), max_length=300, null=True, blank=True)
    created = models.DateTimeField(verbose_name=_('Erstellt am'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Aktualisiert am'), auto_now=True)

    geom = models.PointField(verbose_name='Position', default=Point(0, 0), srid=SRID, null=True, blank=True)

    ''' Creates the geometry field automatically from easting and northing field'''

    def get_geom(self):
        geometry = GEOSGeometry('POINT(%s %s)' % (self.easting, self.northing), srid=SRID)
        return geometry

    def save(self, *args, **kwargs):
        # TODO GEOM ONLY If EASTING + NORTHING Not Null
        if self.easting is None:
            pass
        else:
            self.geom = self.get_geom()
        # if self.qa_clear == 'y':
        #     self.todo_target = 'n'
        # else:
        #     self.todo_target = 'x'
        super(MtlItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.itp_no_mag

    class Meta:
        db_table = 'mtl'
        ordering = ['itp_no_mag']

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
    
fs = OverwriteStorage(location=settings.MEDIA_ROOT)

class MtlItemImage(models.Model):
    def upload_to(self, filename):
        if self.mtl_item.itp_no_mag:
            image_count = MtlItemImage.objects.filter(mtl_item=self.mtl_item).count() + 1
            file_extension = filename.split('.')[-1]
            filename = f"{self.mtl_item.itp_no_mag}_pic_{image_count}.{file_extension}"
        return settings.PROJECT_NAME+'/media/mtlimages/%s' % (filename)
    
    mtl_item = models.ForeignKey(MtlItem, on_delete=models.CASCADE, related_name='mtlimage', null=True, blank=True)

    mtl_item_image = models.ImageField(verbose_name=_('Bild'), null=True, blank=True,
                                       upload_to=upload_to, storage=AMS)

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.main_image)

    image_thumb.allow_tags = True

    def delete(self, *args, **kwargs):
        delete_file(self.mtl_item_image.name)
        if self.mtl_item_image:
            self.mtl_item_image.delete(save=False)

        super(MtlItemImage, self).delete()

    def __str__(self):
        if self.mtl_item_image and hasattr(self.mtl_item_image, 'url'):
            return 'IMG: ' + str(self.mtl_item_image.url)
        else:
            return 'empty'
        
class UnlinkedImage(models.Model):
    def upload_to(self, filename):
        return settings.PROJECT_NAME+'/media/mtlimages/%s' % (filename)

    image = models.ImageField(verbose_name=_('Image'), null=True, blank=True,
                                       upload_to=upload_to, storage=AMS)
    
    notes = models.CharField(verbose_name=_('Notizen'), max_length=200, blank=True, null=True)

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.image)

    image_thumb.allow_tags = True

    def __str__(self):
        if self.image and hasattr(self.image, 'url'):
            return 'IMG: ' + str(self.image.url)
        else:
            return 'empty'
        

DOC_TYPES = [
    ('', ''),
    #('O', _('Overlay')),
    #('T', _('TMI')),
    #('M', _('MBES')),
    #('S', _('SSS')),
]

class Documents(models.Model):
    def overwrite(instance, filename):
        if(instance.type == 'O'):
            return overwrite_duplicate(instance, 'overlay.geojson', 'geodata/vector')
        elif instance.type == 'M':
            file = overwrite_duplicate(instance, 'mbes.tif', 'geodata/tiff')
            return file
        elif instance.type == 'T':
            file = overwrite_duplicate(instance, 'tmi.tif', 'geodata/tiff')
            return file
        elif instance.type == 'S':
            file = overwrite_duplicate(instance, 'sss.tif', 'geodata/tiff')
            return file
        else:
            overwrite_duplicate(instance, filename, 'media/docs')
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name=(_('Name')))
    type = models.CharField(max_length=1, blank=True, null=True, choices=DOC_TYPES, verbose_name=_('Art'))
    file = models.FileField(upload_to=overwrite, null=True, blank=True, storage=AMS, verbose_name=_('Datei'))
    created = models.DateTimeField(verbose_name=_('Erstellt am'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Aktualisiert am'), auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, **kwargs):
        super(Documents, self).save(**kwargs)
        if self.type == 'M':
            upload_xyz('mbes')
        if self.type == 'T':
            upload_xyz('tmi')
        if self.type == 'S':
            upload_xyz('sss')

    class Meta:
        verbose_name_plural = "Documents"


DANGER_LEVEL_CHOICES = [
    ('', ''),
    ('Niedrig', _('Niedrig')),
    ('Mittel', _('Mittel')),
    ('Hoch', _('Hoch')),
]

class Vessel(models.Model):
    def overwrite(instance, filename):
        return overwrite_duplicate(instance, filename, 'vessels')
    
    ship_name = models.CharField(max_length=200, verbose_name=_('Schiffname'), blank=False)
    info_sheet =  models.FileField(upload_to=overwrite, blank=True, null=True, verbose_name=_('Infoblatt'))
    mmsi = models.CharField(max_length=9, verbose_name=_('MMSI'), blank=True, null=True)
    imo = models.CharField(max_length=7, verbose_name=_('IMO'), blank=True, null=True)

    easting = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Easting')
    northing = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Northing')

    geom = models.PointField(verbose_name='Position', default=Point(0, 0), srid=SRID, null=True, blank=True)

    class Meta:
        verbose_name = _('Schiff')
        verbose_name_plural = _('Schiffe')

    def __str__(self):
        return self.ship_name

    def get_geom(self):
        geometry = GEOSGeometry('POINT(%s %s)' % (self.easting, self.northing), srid=SRID)
        return geometry

    def save(self, *args, **kwargs):
        if self.easting is None:
            pass
        else:
            self.geom = self.get_geom()
        
        super(Vessel, self).save(*args, **kwargs)
