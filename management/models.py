from django.contrib.gis.db import models
from datetime import datetime
from backend.blob_actions import overwrite_duplicate, save_pdf
import clearance.settings as settings

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Frame, BaseDocTemplate
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
import json, pdb
from textwrap import wrap

from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.point import Point

from django.core.mail import EmailMessage
from django.contrib.postgres.fields import ArrayField
from datetime import date, timedelta
from django.utils import timezone


SRID = settings.EPSG

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFont('Helvetica', 8)
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        self.drawRightString(211 * mm, 5 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))

class Report(models.Model):
    def overwrite(instance, filename):
            return overwrite_duplicate(instance, filename, 'management/reports')
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    file = models.FileField(upload_to=overwrite, blank=True, null=True, verbose_name=_('Datei'))

    def extract_field_names(self, change_message):
        try:
            change_data = json.loads(change_message)[0]

            if 'changed' in change_data and 'fields' in change_data['changed']:
                return change_data['changed']['fields']
            elif 'added' in change_data:
                return list(change_data['added'].keys())
        except (json.JSONDecodeError, IndexError, KeyError):
            pass

        return []

    def create_report(self, filename='Daily_report.pdf'):
        current_date = datetime.now().date()
        start_of_day = datetime.combine(current_date, datetime.min.time())
        end_of_day = datetime.combine(current_date, datetime.max.time())
        log_entries = LogEntry.objects.filter(action_time__range=(start_of_day, end_of_day))

        def header(canvas, doc):
            canvas.saveState()
            date_str = current_date.strftime('%Y-%m-%d')
            canvas.setFont("Helvetica", 10)
            header = Paragraph(date_str)
            w, h = header.wrap(doc.width, doc.topMargin)
            canvas.drawString(30, doc.pagesize[1] - 20, f"{date_str}")
            canvas.restoreState()

        doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=40)
        elements = []

        data = [['Action Time', 'User', 'Model Type', 'Object ID', 'Object Name', 'Action Flag', 'Changed Fields']]

        for log_entry in log_entries:
            changed_fields = self.extract_field_names(log_entry.change_message)
            changed_fields="\n".join(wrap(', '.join(changed_fields), 40))
            if(not(log_entry.action_flag==2 and changed_fields=='')):
                data.append([
                    log_entry.action_time.strftime('%H:%M'),
                    str(log_entry.user),
                    str(log_entry.content_type.model),
                    log_entry.object_id,
                    log_entry.object_repr,
                    log_entry.get_action_flag_display(),
                    changed_fields, 
                ])

        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        elements.append(table)

        doc.build(elements, onFirstPage=header, onLaterPages=header, canvasmaker=NumberedCanvas)

        save_pdf(filename, 'management/reports/' + str(self.name)+' auto report.pdf')
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.name:
            self.name = datetime.now().strftime('%Y-%m-%d')
        
        self.create_report('tmp/'+str(self.name)+' auto report.pdf')
        self.file = settings.PROJECT_NAME+'/management/reports/' + str(self.name)+' auto report.pdf'

        super().save(*args, **kwargs)

EVENT_TYPES = [
    ('', ''),
    ('W', _('Weather Downtime')),
    ('T', _('Scheduled Target')),
    ('C', _('Crew Change')),
    ('P', _('Port Call')),
    ('0', _('Other'))
]

class CalendarEvents(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True, choices=EVENT_TYPES)
    
    def __str__(self):
        return self.title+" from "+str(self.start)+" to "+str(self.end)
    
    class Meta:
        verbose_name_plural = "Calendar Events"
    
'''
DOC_TYPES = [
    ('', ''),
    ('WMS', _('Work Method Statemet')),
    ('SOP', _('Standard Operation Procedure')),
    ('EQI', _('Equipment Info')),
    ('PJI', _('Project Info')),
    ('PSI', _('Personnel Info'))
    ('PMT', _('Permits'))
    ('KOF', _('Kickoff Files'))

    ('HIR', _('Hazard Identification and Risk Assessment'))

]
'''

class Documents(models.Model):
    def overwrite(instance, filename):
        overwrite_duplicate(instance, filename, 'management/docs')

    name = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('Name'))
    file = models.FileField(upload_to=overwrite, blank=True, null=True, verbose_name=_('Datei'))
    type = models.CharField(max_length=50, blank=True, null=True)
    uploaded = models.DateTimeField(verbose_name=_('Hochgeladen am'), blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Documents"

class OperationalHours(models.Model):
    date = models.DateField(verbose_name=_('Datum'), blank=False)
    hours = models.IntegerField(verbose_name=_('Betriebsstunden'), blank=False)
    comment = models.TextField(verbose_name=_('Kommentar'), max_length=250, blank=True, null=True)

    def __str__(self):
        return str(self.date)
    
    class Meta:
        verbose_name_plural = "Operational Hours"

ORDER_STATUS_CHOICES = [
    ('', ''),
    ('Offen', _('Offen')),
    ('wird bearbeitet', _('wird bearbeitet')),
    ('Bestellt', _('Bestellt')),
    ('Auf Lager', _('Auf Lager')),
    ('Versandfertig', _('Versandfertig')),
    ('Erhalten', _('Erhalten')),
]

class Orders(models.Model):
    def send_notification_email(self):
        message = f"Guten Tag,\n\nEine neue Bestellung für \"{self.title}\" für Projekt {settings.PROJECT_NAME} wurde erstellt. Bitte prüfen Sie die Bestellung und aktualisieren Sie den Bestellstatus gegebenenfalls unter {settings.URL}/admin/management/orders.\n\nDiese Nachricht wurde automatisch generiert. Bitte antworten Sie nicht auf diese E-Mail."
        to_list = ["h.bauermann@seaterra.de", "b.raupers@seaterra.de", "n.emini@seaterra.de", "kd.golla@seaterra.de"]
        msg = EmailMessage(
            subject=f"Notifikation für die Erstellung von Bestellungen für Projekt " + settings.PROJECT_NAME,
            body=message,
            from_email='seaterra.lagerportal@gmail.com',
            to=to_list,
        )
        msg.send()
    title = models.CharField(max_length=255, verbose_name=_('Titel'), blank=False)
    ship = models.CharField(max_length=255, verbose_name=_('Schiff'), blank=True, null=True)
    order_date = models.DateField(verbose_name=_('Bestelldatum'), blank=True, null=True)
    ordered_by = models.CharField(max_length=255, verbose_name=_('Besteller'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Beschreibung'), blank=True, null=True)
    count = models.IntegerField(verbose_name=_('Anzahl'), blank=True, null=True)
    link = models.URLField(verbose_name=_('Link'), blank=True, null=True)
    image = models.ImageField(upload_to='management/orders/', blank=True, null=True, verbose_name=_('Bild'))
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='', verbose_name=_('Status'), blank=True, null=True)
    overseer = models.CharField(max_length=255, verbose_name="Bearbeiter", blank=True, null=True)
    delivery_date = models.DateField(verbose_name=_('Lieferdatum'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.send_notification_email()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Bestellung")
        verbose_name_plural = _("Bestellungen")

class DPRs(models.Model):
    def default_vessel():
        return "Aquarius-G"
    def default_client():
        return "Amprion Offshore GmbH"
    def default_contractor():
        return "SeaTerra GmbH"
    def default_callsign():
        return "PIPS"
    def default_project():
        return "OSS DW_Delta & OSS BW_Delta"
    def default_task():
        return "Marine Geophysical UXO Investigation and Clearance"
    def default_ceo():
        return {'name': 'Edgar Schwab', 'number': '+491604715580'}
    def default_pm():
        return {'name': 'Dieter Guldin', 'number': '+491713304543'}
    def default_ocm():
        return {'name': 'Goran Maric', 'number': '+4915127473476'}
    def default_eod():
        return {'name': 'Tjerk Reichel', 'number': '+491604715577'}
    def default_captain():
        return {'name': 'Niels Robben', 'number': '+31652652705'}
    def default_client_rep():
        return {'name': 'Maciel Sobol', 'number': '+48796731880'}
    def default_vessel_email():
        return 'aquariusg.captain@n-sea.com'
    def default_dist_list():
        return ['helge.vosberg@amprion.net', 'justus.maas@amprion.net',
                'e.schwab@seaterra.de', 'd.guldin@seaterra.de',
                'b.raupers@seaterra.de', 'u.schneider@seaterra.de',
                'k.renken@seaterra.de']
    def default_weather_info():
        return [{'time': '0:00', 'max_wave_today': '', 'max_wave_tomorrow': ''}, {'time': '6:00', 'max_wave_today': '', 'max_wave_tomorrow': ''}, 
                {'time': '12:00', 'max_wave_today': '', 'max_wave_tomorrow': ''}, {'time': '18:00', 'max_wave_today': '', 'max_wave_tomorrow': ''}]
    def default_weather_info_lookahead():
        return [{'time': '0:00', '48hrs': '', '72hrs': ''}, {'time': '12:00', '48hrs': '', '72hrs': ''}]
    def default_project_start():
        return date(2025, 7, 4)
    def default_work_entries():
        return [{'target_id': '', 'description': '', 'object': ''}]
    def default_daily_routine():
        return [{'from': '', 'to': '', 'duration': '', 'category': '', 'target_id': '', 'description': ''}]
    def duration_from_string(duration):
        try:
            hours, minutes = map(int, duration.split(":"))
            return timedelta(hours=hours, minutes=minutes)
        except (ValueError, AttributeError):
            return timedelta()
    def latest_dpr(self):
        latest_dpr = DPRs.objects.exclude(date__gte=self.date).order_by('-date').first()
        return latest_dpr
    date = models.DateField(verbose_name=_('Datum'), blank=False)
    vessel = models.CharField(max_length=255, verbose_name=_('Vessel'), blank=True, null=True, default=default_vessel)
    client = models.CharField(max_length=255, verbose_name=_('Client'), blank=True, null=True, default=default_client)
    contractor = models.CharField(max_length=255, verbose_name=_('Contractor'), blank=True, null=True, default=default_contractor)
    callsign = models.CharField(max_length=10, verbose_name=('Call Sign'), blank=True, null=True, default=default_callsign)
    project = models.CharField(max_length=255, verbose_name=('Project'), blank=True, null=True, default=default_project)
    task = models.CharField(max_length=255, verbose_name=('Task'), blank=True, null=True, default=default_task)
    position_at_2400 = models.TextField(verbose_name=_('Position at 24:00LT'), blank=True, null=True)
    
    ceo = models.JSONField(verbose_name=_('CEO'), default=default_ceo, blank=True, null=True)
    project_manager = models.JSONField(verbose_name=_('Project Manager'), default=default_pm, blank=True, null=True)
    ocm = models.JSONField(verbose_name=_('OCM'), default=default_ocm, blank=True, null=True)
    eod_manager = models.JSONField(verbose_name=_('EOD Manager'), default=default_eod, blank=True, null=True)
    captain = models.JSONField(verbose_name=_('Captain'), default=default_captain, blank=True, null=True)
    client_rep = models.JSONField(verbose_name=_('Client Rep'), default=default_client_rep, blank=True, null=True)
    vessel_email = models.EmailField(verbose_name=_('Vessel Email'), default=default_vessel_email, blank=True, null=True)

    distribution_list = ArrayField(base_field=models.EmailField(), verbose_name=_('Distribution List'), blank=True, null=True, default=default_dist_list)

    marine_onsigners = ArrayField(base_field=models.CharField(max_length=255), verbose_name=_('Marine Onsigners'), blank=True, null=True, default=list)
    seaterra_onsigners = ArrayField(base_field=models.CharField(max_length=255), verbose_name=_('SeaTerra Onsigners'), blank=True, null=True, default=list)
    client_onsigners = ArrayField(base_field=models.CharField(max_length=255), verbose_name=_('Client Onsigners'), blank=True, null=True, default=list)

    marine_offsigners = ArrayField(base_field=models.CharField(max_length=255), verbose_name=_('Marine Offsigners'), blank=True, null=True, default=list)
    seaterra_offsigners = ArrayField(base_field=models.CharField(max_length=255), verbose_name=_('SeaTerra Offsigners'), blank=True, null=True, default=list)
    client_offsigners = ArrayField(base_field=models.CharField(max_length=255), verbose_name=_('Client Offsigners'), blank=True, null=True, default=list)

    weather_info = models.JSONField(verbose_name=_('Weather Info'), blank=True, null=True, default=default_weather_info)
    weather_info_lookahead = models.JSONField(verbose_name=_('Weather Info Lookahead'), blank=True, null=True, default=default_weather_info_lookahead)

    hse_meetings = models.IntegerField(verbose_name=_('HSE Meetings'), blank=True, null=True, default=0)
    hse_toolbox_talks = models.IntegerField(verbose_name=_('HSE Toolbox Talks'), blank=True, null=True, default=0)
    hse_safety_observation_form = models.IntegerField(verbose_name=_('HSE Safety Observation Form'), blank=True, null=True, default=0)
    hse_safety_drills = models.IntegerField(verbose_name=_('HSE Safety Drills'), blank=True, null=True, default=0)
    hse_incidents = models.IntegerField(verbose_name=_('HSE Incidents'), blank=True, null=True, default=0)
    hse_accidents = models.IntegerField(verbose_name=_('HSE Accidents'), blank=True, null=True, default=0)
    hse_working_hours = models.IntegerField(verbose_name=_('HSE Working Hours'), blank=True, null=True)
    hse_start = models.DateField(verbose_name=_('HSE Start of Project'), blank=True, null=True, default=default_project_start)
    hse_days_without_accident = models.IntegerField(verbose_name=_('HSE Days Without Accident'), blank=True, null=True, default=1)

    hse_meetings_total = models.IntegerField(verbose_name=_('HSE Meetings Total'), blank=True, null=True, default=0)
    hse_toolbox_talks_total = models.IntegerField(verbose_name=_('HSE Toolbox Talks Total'), blank=True, null=True, default=0)
    hse_safety_observation_form_total = models.IntegerField(verbose_name=_('HSE Safety Observation Form Total'), blank=True, null=True, default=0)
    hse_safety_drills_total = models.IntegerField(verbose_name=_('HSE Safety Drills Total'), blank=True, null=True, default=0)
    hse_incidents_total = models.IntegerField(verbose_name=_('HSE Incidents Total'), blank=True, null=True, default=0)
    hse_accidents_total = models.IntegerField(verbose_name=_('HSE Accidents Total'), blank=True, null=True, default=0)
    hse_working_hours_total = models.IntegerField(verbose_name=_('HSE Working Hours Total'), blank=True, null=True)
    hse_days_without_accident_total = models.IntegerField(verbose_name=_('HSE Days Without Accident Total'), blank=True, null=True, default=1)

    work_summary = models.TextField(verbose_name=_('Work Summary'), blank=True, null=True)
    work_entries = models.JSONField(verbose_name=_('Work Entries'), blank=True, null=True, default=default_work_entries)

    plan_24hrs = models.TextField(verbose_name=_('Plan for the next 24hrs'), blank=True, null=True)

    daily_routine = models.JSONField(verbose_name=_('Daily Routine'), blank=True, null=True, default=default_daily_routine)

    routine_vessel = models.CharField(max_length=255, verbose_name=_('Routine Vessel'), blank=True, null=True)
    routine_total_targets = models.IntegerField(verbose_name=_('Routine Total Targets'), blank=True, null=True)
    routine_cleared_targets = models.IntegerField(verbose_name=_('Routine Cleared Targets'), blank=True, null=True)
    routine_remaining_targets = models.IntegerField(verbose_name=_('Routine Remaining Targets'), blank=True, null=True)
    routine_total_uxos_found = models.IntegerField(verbose_name=_('Routine Total UXOs Found'), blank=True, null=True)
    routine_targets_cleared_today = models.IntegerField(verbose_name=_('Routine Targets Cleared Today'), blank=True, null=True)
    routine_remarks = models.TextField(verbose_name=_('Routine Remarks'), blank=True, null=True)

    mob_duration = models.CharField(max_length=10, verbose_name=_('MOB Duration'), blank=True, null=True, default="00:00")
    t_duration = models.CharField(max_length=10, verbose_name=_('Transit Duration'), blank=True, null=True, default="00:00")
    i_duration = models.CharField(max_length=10, verbose_name=_('Survey Spread Duration'), blank=True, null=True, default="00:00")
    cs_duration = models.CharField(max_length=10, verbose_name=_('Client Standby Duration'), blank=True, null=True, default="00:00")
    wdt_duration = models.CharField(max_length=10, verbose_name=_('Weather Downtime Duration'), blank=True, null=True, default="00:00")
    tbw_duration = models.CharField(max_length=10, verbose_name=_('Time Based Work Duration'), blank=True, null=True, default="00:00")
    cc_duration = models.CharField(max_length=10, verbose_name=_('Crew Change Duration'), blank=True, null=True, default="00:00")
    tdt_duration = models.CharField(max_length=10, verbose_name=_('Technical Downtime Duration'), blank=True, null=True, default="00:00")
    total_duration = models.CharField(max_length=10, verbose_name=('Total Duration'), blank=True, null=True, default="00:00")

    mob_duration_total = models.CharField(max_length=10, verbose_name=_('MOB Duration Total'), blank=True, null=True, default="00:00")
    t_duration_total = models.CharField(max_length=10, verbose_name=_('Transit Duration Total'), blank=True, null=True, default="00:00")
    i_duration_total = models.CharField(max_length=10, verbose_name=_('Survey Spread Duration Total'), blank=True, null=True, default="00:00")
    cs_duration_total = models.CharField(max_length=10, verbose_name=_('Client Standby Duration Total'), blank=True, null=True, default="00:00")
    wdt_duration_total = models.CharField(max_length=10, verbose_name=_('Weather Downtime Duration Total'), blank=True, null=True, default="00:00")
    tbw_duration_total = models.CharField(max_length=10, verbose_name=_('Time Based Work Duration Total'), blank=True, null=True, default="00:00")
    cc_duration_total = models.CharField(max_length=10, verbose_name=_('Crew Change Duration Total'), blank=True, null=True, default="00:00")
    tdt_duration_total = models.CharField(max_length=10, verbose_name=_('Technical Downtime Duration Total'), blank=True, null=True, default="00:00")
    total_duration_total = models.CharField(max_length=10, verbose_name=('Total Duration Total'), blank=True, null=True, default="00:00")

    weather_interpretation = models.TextField(verbose_name=_('Interpretation of weather forecast'), blank=True, null=True)
    technical_issues = models.TextField(verbose_name=_('Technical Issues'), blank=True, null=True)
    meetings = models.TextField(verbose_name=_('Meetings'), blank=True, null=True)
    other_remarks = models.TextField(verbose_name=_('Other'), blank=True, null=True)

    seaterra_comments = models.TextField(verbose_name=_('SeaTerra Comments'), blank=True, null=True)
    client_comments = models.TextField(verbose_name=_('Client Comments'), blank=True, null=True)

    def __str__(self):
        return str(self.date) + " DPR"
    
    class Meta:
        verbose_name = _("DPR")
        verbose_name_plural = _("DPRs")

    def load_totals(self):
        if self.latest_dpr():
            self.hse_meetings_total = self.latest_dpr().hse_meetings_total
            self.hse_toolbox_talks_total = self.latest_dpr().hse_toolbox_talks_total
            self.hse_safety_observation_form_total = self.latest_dpr().hse_safety_observation_form_total
            self.hse_safety_drills_total = self.latest_dpr().hse_safety_drills_total
            self.hse_incidents_total = self.latest_dpr().hse_incidents_total
            self.hse_accidents_total = self.latest_dpr().hse_accidents_total
            self.hse_working_hours_total = self.latest_dpr().hse_working_hours_total
            self.hse_days_without_accident_total = self.latest_dpr().hse_days_without_accident_total

            self.mob_duration_total = self.latest_dpr().mob_duration_total
            self.t_duration_total = self.latest_dpr().t_duration_total
            self.i_duration_total = self.latest_dpr().i_duration_total
            self.cs_duration_total = self.latest_dpr().cs_duration_total
            self.wdt_duration_total = self.latest_dpr().wdt_duration_total
            self.tbw_duration_total = self.latest_dpr().tbw_duration_total
            self.cc_duration_total = self.latest_dpr().cc_duration_total
            self.tdt_duration_total = self.latest_dpr().tdt_duration_total
            self.total_duration_total = self.latest_dpr().total_duration_total

    def save(self, *args, **kwargs):
        if not self.pk:
            self.load_totals()

        super().save(*args, **kwargs)
