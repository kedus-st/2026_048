from django.urls import path

from . import views

urlpatterns = [
    path('calendar', views.calendar, name='calendar'),
    path('schedule_event', views.schedule_event, name='schedule_event'),
    path('documents', views.documents, name='documents'),
    path('doc_upload', views.doc_upload, name='doc_upload'),
    path("weather", views.weather, name='weather'),
    path('progress-reports', views.dprs, name='progress-reports'),
    path("dprs/get-report", views.get_report, name="get_report"),
    path("dprs/save-report", views.save_report, name="save_report"),
    path("dprs/reload-totals", views.reload_totals, name="reload_totals"),
    path("dprs/reset-dpr", views.reset_dprs, name="reset_dprs"),
    path("dprs/print-dpr", views.print_dpr, name="print_dpr"),
    path("dprs/copy-dpr", views.copy_dpr, name="copy_dpr"),
    path("dpr-statistics", views.dpr_statistics, name='dpr_statistics'),
]