from django.contrib import admin, messages
from management.models import Report, CalendarEvents, Documents, OperationalHours, Orders, DPRs
from import_export.admin import ImportExportMixin, ImportExportActionModelAdmin
from django.shortcuts import render, redirect
from clearance.settings import URL
from clearance.settings import PROJECT_NAME
from management.resources import OrdersResource
from .forms import EmailActionForm
from django.core.mail import EmailMessage

admin.site.register(Report)
admin.site.register(CalendarEvents)

@admin.register(OperationalHours)
class OperationalHoursAdmin(ImportExportMixin, ImportExportActionModelAdmin):
    model = OperationalHours
    save_on_top = True

    list_display = ('date', 'hours', 'comment')

admin.site.register(Documents)

def send_email_action(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = EmailActionForm(request.POST)
        if form.is_valid():
            to_list = form.cleaned_data["to"]
            cc_list = form.cleaned_data["cc"]
            message = "Guten Tag,\n\nEs wurde eine Anfrage gestellt, Sie an die folgenden Artikel zu erinnern:\n\n"

            for obj in queryset:
                message += f"- {obj.title}\n"

            message += f"\nBitte prüfen Sie den Bestellstatus dieser Artikel unter {URL}/admin/management/orders und aktualisieren Sie ihn gegebenenfalls.\n\nDiese Nachricht wurde automatisch generiert. Bitte antworten Sie nicht auf diese E-Mail."

            #send_mail(
            #    subject=f"Erinnerung an Bestellungen für Projekt " + PROJECT_NAME,
            #    message=message,
            #    from_email='seaterra.lagerportal@gmail.com',
            #    recipient_list=to_list,
            #    cc=cc_list,
            #)
            msg = EmailMessage(
                subject=f"Erinnerung an Bestellungen für Projekt " + PROJECT_NAME,
                body=message,
                from_email='seaterra.lagerportal@gmail.com',
                to=to_list,
                cc=cc_list,
            )
            msg.send()
            messages.success(request, f"Email an {', '.join(to_list)} für {queryset.count()} Artikel gesendet.")
            return redirect(request.get_full_path())
    else:
        form = EmailActionForm()

    return render(request, 'admin/send_email_action.html', context={
        'items': queryset,
        'form': form,
        'action': 'send_email_action',
        'opts': modeladmin.model._meta,
        'queryset': queryset,
    })

send_email_action.short_description = "Erinnerung an ausgewählte Artikel senden"

#@admin.register(Orders)
class OrdersAdmin(ImportExportMixin, ImportExportActionModelAdmin):
    model = Orders
    save_on_top = True

    resource_class = OrdersResource

    list_filter = ('ship', 'order_date', 'ordered_by', 'status', 'overseer')
    list_display = ('title', 'ship', 'order_date', 'ordered_by', 'status',  'overseer', 'description', 'count', 'link', 'delivery_date')
    #list_editable = ('ship', 'order_date', 'ordered_by', 'status', 'count', 'link', 'delivery_date')
    list_editable = ('status',  'overseer', 'delivery_date')
    search_fields = ('title', 'ship', 'ordered_by', 'description', 'link')

    actions = [send_email_action]

admin.site.register(DPRs)