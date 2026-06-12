
import os
from django.http import HttpResponse
from management.models import DPRs

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Image, SimpleDocTemplate
from textwrap import wrap
from reportlab.platypus import Spacer, HRFlowable, KeepTogether

def contact_details_span(start, rows):
    span = []
    for i in range(start, start + rows):
        span.append(('SPAN', (0, i), (1, i)))
        span.append(('SPAN', (2, i), (3, i)))
        span.append(('SPAN', (4, i), (5, i)))
        span.append(('SPAN', (7, i), (12, i)))
    return span

def wrap_(string, width):
    if string is None:
        string = ''
    return "\n".join(wrap(string, width=width))

def format_ddmmyyyy(date_obj):
    if not date_obj:
        return ''
    return date_obj.strftime('%d/%m/%Y')

def generate_dpr_pdf(report_date):
    dpr = DPRs.objects.filter(date=report_date).first()
    if not dpr:
        raise ValueError(f"No DPR found for date '{report_date}'.")
    
    file_path = 'tmp/' + str(dpr.date) + ' DPR.pdf'

    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm, topMargin=10 * mm,
                            bottomMargin=10 * mm)
    doc.pagesize = portrait(A4)
    elements = []
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))

    address = 'SeaTerra GmbH Geophysics & EOD Services\nAn der Trift 21, D-16348 Wandlitz, Germany\nTel:+49(0)33397-29727, Fax:+49(0)33397-29729'
    logo = Image('static/img/seaterra_logo.png', width=40*mm, height=28*mm)
    header_data = [
        ['Daily Progress Report', '', ''],
        ['Marine UXO Investigation & Clearance', address, logo],
        [dpr.project, '', ''],
        [dpr.vessel, '', '']
    ]

    header_style = TableStyle([
        ('SPAN', (0, 0), (2,0)), ('FONTSIZE', (0, 0), (2,0), 18), ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
        ('SPAN', (0, 1), (0,1)), ('SPAN', (1, 1), (1,3)), ('SPAN', (2, 1), (2, 3)), ('FONTSIZE', (1, 1), (1,3), 7), ('ALIGN', (1, 1), (1, 3), 'RIGHT'),
        ('SPAN', (0, 2), (1,2)),
        ('SPAN', (0, 3), (0,3)),
    ])
    header_table = Table(header_data,
                         colWidths=[90*mm, 60*mm, 40*mm],
                         rowHeights=[10*mm, 9*mm, 9*mm, 9*mm])
    header_table.setStyle(header_style)
    elements.append(header_table)
    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=3, color=colors.black))
    elements.append(Spacer(1, 15))

    sub_header_data = [
        ['Client:', dpr.client, '', 'Date:', format_ddmmyyyy(dpr.date)],
        ['Contractor:', dpr.contractor, '', 'Project:', dpr.project],
        ['Vessel:', str(dpr.vessel) + '       Call Sign: ' + str(dpr.callsign), '', 'Task:', dpr.task]
    ]
    sub_header_style = TableStyle([
        ('SPAN', (0, 0), (0, 0)), ('SPAN', (1, 0), (2, 0)), ('SPAN', (3, 0), (3, 0)), ('SPAN', (4, 0), (4, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (1, 1), (2, 1)), ('SPAN', (3, 1), (3, 1)), ('SPAN', (4, 1), (4, 1)),
        ('SPAN', (0, 2), (0, 2)), ('SPAN', (1, 2), (1, 2)), ('SPAN', (2, 2), (2, 2)), ('SPAN', (3, 2), (3, 2)), ('SPAN', (4, 2), (4, 2)),
    ])
    sub_header_table = Table(sub_header_data,
                             colWidths=[30*mm, 40*mm, 30*mm, 15*mm, 85*mm],
                             rowHeights=[5*mm]*3)
    sub_header_table.setStyle(sub_header_style)
    elements.append(sub_header_table)
    elements.append(Spacer(1, 15))

    dark_blue = colors.Color(47/255, 117/255, 181/255)
    light_blue = colors.Color(189/255, 215/255, 238/255)

    group1_data = [
        ['A. Contact Details', '2', '3', '4', '5', '6', '', 'Vessel ' + str(dpr.vessel) + ' Position at 24:00LT', '9', '10', '11', '12', '13'],
        ['CEO:', '2', dpr.ceo.get('name', ''), '4', dpr.ceo.get('number', ''), '6', '', dpr.position_at_2400 or '', '9', '10', '11', '12', '13'],
        ['Project Manager:', '2', dpr.project_manager.get('name', ''), '4', dpr.project_manager.get('number', ''), '6', '', 'Distribution List', '9', '10', '11', '12', '13'],
        ['OCM:', '2', dpr.ocm.get('name', ''), '4', dpr.ocm.get('number', ''), '6', '', dpr.distribution_list[0] or '', '9', '10', '11', '12', '13'],
        ['EOD Manager:', '2', dpr.eod_manager.get('name', ''), '4', dpr.eod_manager.get('number', ''), '6', '', dpr.distribution_list[1] or '', '9', '10', '11', '12', '13'],
        [wrap_('Captain / Tel.Vessel:', 20), '2', dpr.captain.get('name', ''), '4', dpr.captain.get('number', ''), '6', '', dpr.distribution_list[2] or '', '9', '10', '11', '12', '13'],
        [wrap_('Client Representative:', 20), '2', dpr.client_rep.get('name', ''), '4', dpr.client_rep.get('number', ''), '6', '', dpr.distribution_list[3] or '', '9', '10', '11', '12', '13'],
        ['E-Mail Vessel:', '2', dpr.vessel_email, '4', '5', '6', '', dpr.distribution_list[4] or '', '8', '9', '10', '11', '12']
    ]
    group1_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (5, 0)), ('SPAN', (7, 0), (12, 0)),
        ('SPAN', (0, 7), (1, 7)), ('SPAN', (2, 7), (5, 7)), ('SPAN', (7, 7), (12, 7)), #Final contact details row with vessel email
        ('BACKGROUND', (0, 0), (5, 0), dark_blue),
        ('BACKGROUND', (7, 0), (12, 0), light_blue),
        ('BACKGROUND', (7, 2), (12, 2), dark_blue),
    ])

    for span in contact_details_span(1, 6):
        group1_style.add(*span)

    if len(dpr.distribution_list) > 5:
        for recipient in dpr.distribution_list[5:]:
            group1_data.append(['', '2', '', '4', '5', '6', '', recipient or '', '9', '10', '11', '12', '13'])
            group1_style.add('SPAN', (0, len(group1_data)-1), (5, len(group1_data)-1))
            group1_style.add('SPAN', (7, len(group1_data)-1), (12, len(group1_data)-1))

    group1_style.add('SPAN', (6, 0), (6, len(group1_data)-1))#Middle empty column 7

    group1_table = Table(group1_data, colWidths=[15*mm]*13)
    group1_table.setStyle(group1_style)

    elements.append(group1_table)
    elements.append(Spacer(1, 15))

    group2_data = [
        ['B. Personnel', '2', '3', '4', '5', '6', '', '8', '9', '10', '11', '12', '13'],
        ['Onsigners', '2', '3', '4', '5', '6', '', 'Offsigners', '9', '10', '11', '12', '13'],
        ['Marine Crew', '2', 'SeaTerra', '4', 'Client', '6', '', 'Marine Crew', '9', 'SeaTerra', '11', 'Client', '13'],
    ]
    personnel_list_length = max(len(dpr.marine_onsigners), len(dpr.seaterra_onsigners),
                                len(dpr.client_onsigners), len(dpr.marine_offsigners),
                                len(dpr.seaterra_offsigners), len(dpr.client_offsigners))
    
    
    group2_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (12, 0)),
        ('SPAN', (0, 1), (5, 1)), ('SPAN', (7, 1), (12, 1)),
        ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (3, 2)), ('SPAN', (4, 2), (5, 2)), ('SPAN', (7, 2), (8, 2)), ('SPAN', (9, 2), (10, 2)), ('SPAN', (11, 2), (12, 2)),
        ('BACKGROUND', (0, 0), (12, 0), dark_blue),
        ('BACKGROUND', (0, 1), (5, 1), light_blue), ('BACKGROUND', (7, 1), (12, 1), light_blue),
        ('BACKGROUND', (0, 1), (5, 2), light_blue), ('BACKGROUND', (7, 2), (12, 2), light_blue),
    ])

    for i in range(personnel_list_length):
        group2_data.append([
            wrap_((((dpr.marine_onsigners   or [])[i:i+1] or [''])[0]) or '', 15), '2',
            wrap_((((dpr.seaterra_onsigners or [])[i:i+1] or [''])[0]) or '', 15), '4',
            wrap_((((dpr.client_onsigners   or [])[i:i+1] or [''])[0]) or '', 15), '6', '',
            wrap_((((dpr.marine_offsigners  or [])[i:i+1] or [''])[0]) or '', 15), '9',
            wrap_((((dpr.seaterra_offsigners or [])[i:i+1] or [''])[0]) or '', 15), '11',
            wrap_((((dpr.client_offsigners  or [])[i:i+1] or [''])[0]) or '', 15), '13',
        ])
        group2_style.add('SPAN', (0, len(group2_data)-1), (1, len(group2_data)-1))
        group2_style.add('SPAN', (2, len(group2_data)-1), (3, len(group2_data)-1))
        group2_style.add('SPAN', (4, len(group2_data)-1), (5, len(group2_data)-1))
        group2_style.add('SPAN', (7, len(group2_data)-1), (8, len(group2_data)-1))
        group2_style.add('SPAN', (9, len(group2_data)-1), (10, len(group2_data)-1))
        group2_style.add('SPAN', (11, len(group2_data)-1), (12, len(group2_data)-1))
    
    group2_style.add('SPAN', (6, 1), (6, len(group2_data)-1))#Middle empty column 7

    group2_table = Table(group2_data, colWidths=[15*mm]*13)
    group2_table.setStyle(group2_style)

    elements.append(KeepTogether(group2_table))
    elements.append(Spacer(1, 15))

    group3_data = [
        ['C. Weather Info (weather forecast StormGeo 06:00 LT)', '', '3', '4', '5', '6', '', 'D. HSE Records', '9', '10', '11', '12', '13'],
        ['', '2', 'Today\n[max wave m]', '4', 'Tomorrow\n[max wave m]', '6', '', '', '9', 'Today', '11', 'Accumulated Total', '13'],
        [dpr.weather_info[0].get('time', ''), '2', dpr.weather_info[0].get('today_max_wave', ''), '4', dpr.weather_info[0].get('tomorrow_max_wave', ''), '6', '', 'Daily Meetings', '9', dpr.hse_meetings, '11', dpr.hse_meetings_total, '13'],
        [dpr.weather_info[1].get('time', ''), '2', dpr.weather_info[1].get('today_max_wave', ''), '4', dpr.weather_info[1].get('tomorrow_max_wave', ''), '6', '', 'Toolbox Talks', '9', dpr.hse_toolbox_talks, '11', dpr.hse_toolbox_talks_total, '13'],
        [dpr.weather_info[2].get('time', ''), '2', dpr.weather_info[2].get('today_max_wave', ''), '4', dpr.weather_info[2].get('tomorrow_max_wave', ''), '6', '', wrap_('Safety Observation Form', 15), '9', dpr.hse_safety_observation_form, '11', dpr.hse_safety_observation_form_total, '13'],
        [dpr.weather_info[3].get('time', ''), '2', dpr.weather_info[3].get('today_max_wave', ''), '4', dpr.weather_info[3].get('tomorrow_max_wave', ''), '6', '', 'Safety Drills', '9', dpr.hse_safety_drills, '11', dpr.hse_safety_drills_total, '13'],
        ['Lookahead', '2', '48 hours', '4', '72 hours', '6', '', 'Incidents', '9', dpr.hse_incidents, '11', dpr.hse_incidents_total, '13'],
        [dpr.weather_info_lookahead[0].get('time', ''), '2', dpr.weather_info_lookahead[0].get('today_max_wave', ''), '4', dpr.weather_info_lookahead[0].get('tomorrow_max_wave', ''), '6', '', 'Accidents', '9', dpr.hse_accidents, '11', dpr.hse_accidents_total, '13'],
        [dpr.weather_info_lookahead[1].get('time', ''), '2', dpr.weather_info_lookahead[1].get('today_max_wave', ''), '4', dpr.weather_info_lookahead[1].get('tomorrow_max_wave', ''), '6', '', 'Working Hours', '9', dpr.hse_working_hours, '11', dpr.hse_working_hours_total, '13'],
        ['', '2', '3', '4', '5', '6', '', 'Start of Project', '9', format_ddmmyyyy(dpr.hse_start), '11', (dpr.date - dpr.hse_start).days if dpr.date and dpr.hse_start else '', '13'],
        ['1', '2', '3', '4', '5', '6', '', wrap_('Days without Accident', 15), '9', dpr.hse_days_without_accident, '11', dpr.hse_days_without_accident_total, '13'],
    ]

    group3_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (5, 0)), ('SPAN', (7, 0), (12, 0)),
        ('BACKGROUND', (0, 0), (5, 0), dark_blue), ('BACKGROUND', (7, 0), (12, 0), dark_blue),
        ('BACKGROUND', (0, 1), (5, 1), dark_blue), ('BACKGROUND', (7, 1), (12, 1), dark_blue),
        ('BACKGROUND', (7, 2), (8, 10), light_blue),
        ('BACKGROUND', (0, 6), (5, 6), light_blue)
    ])
    for i in range(1, 9):
        group3_style.add('SPAN', (0, i), (1, i))
        group3_style.add('SPAN', (2, i), (3, i))
        group3_style.add('SPAN', (4, i), (5, i))
        group3_style.add('SPAN', (7, i), (8, i))
        group3_style.add('SPAN', (9, i), (10, i))
        group3_style.add('SPAN', (11, i), (12, i))

    group3_style.add('SPAN', (6, 0), (6, 8))#Middle empty column 7

    group3_style.add('SPAN', (0, 9), (6, 10))
    group3_style.add('SPAN', (7, 9), (8, 9))
    group3_style.add('SPAN', (9, 9), (10, 9))
    group3_style.add('SPAN', (11, 9), (12, 9))

    group3_style.add('SPAN', (7, 10), (8, 10))
    group3_style.add('SPAN', (9, 10), (10, 10))
    group3_style.add('SPAN', (11, 10), (12, 10))

    group3_table = Table(group3_data, colWidths=[15*mm]*13)
    group3_table.setStyle(group3_style)

    elements.append(KeepTogether(group3_table))
    elements.append(Spacer(1, 15))

    group4_data = [
        ['E. Summary of Works Carried Out Today', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
        [dpr.work_summary, '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
        ['Target Cleared (ID)', '2', 'Description', '4', '5', '6', '7', '8', '9', '10', '11', 'Object', '13'],
    ]

    group4_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (12, 0)),
        ('SPAN', (0, 1), (12, 1)),
        ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (10, 2)), ('SPAN', (11, 2), (12, 2)),
        ('BACKGROUND', (0, 0), (12, 0), dark_blue),
        ('BACKGROUND', (0, 2), (12, 2), light_blue),
    ])

    for i in range(0, len(dpr.work_entries)):
        group4_data.append([dpr.work_entries[i].get('target_id', ''), '2', wrap_(dpr.work_entries[i].get('description', ''), 15*9), '4', '5', '6', '7', '8', '9', '10', '11', wrap_(dpr.work_entries[i].get('object', ''), 15*2), '13'])
        group4_style.add('SPAN', (0, i+3), (1, i+3))
        group4_style.add('SPAN', (2, i+3), (10, i+3))
        group4_style.add('SPAN', (11, i+3), (12, i+3))

    group4_table = Table(group4_data, colWidths=[15*mm]*13)
    group4_table.setStyle(group4_style)

    elements.append(KeepTogether(group4_table))
    elements.append(Spacer(1, 15))

    group5_data = [
        ['F. Plan For Next 24h', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
        [wrap_(dpr.plan_24hrs, 15*13), '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'],
    ]

    group5_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (12, 0)),
        ('SPAN', (0, 1), (12, 1)),
        ('BACKGROUND', (0, 0), (12, 0), dark_blue)
    ])

    group5_table = Table(group5_data, colWidths=[15*mm]*13)
    group5_table.setStyle(group5_style)

    elements.append(KeepTogether(group5_table))
    elements.append(Spacer(1, 15))

    group6_data = [
        ['G. Chronological Daily Routine', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
        ['From', '2', 'To', '4', 'Duration(hh:mm)', '6', 'Category', '8', 'Target ID', '10', 'Description', '12', '13', '14'],
    ]

    group6_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (13, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)), ('SPAN', (8, 1), (9, 1)), ('SPAN', (10, 1), (13, 1)),
        ('BACKGROUND', (0, 0), (13, 0), dark_blue),
        ('BACKGROUND', (0, 1), (13, 1), light_blue),
    ])

    for i in range(len(dpr.daily_routine)):
        group6_data.append([dpr.daily_routine[i].get('from', ''), '2', dpr.daily_routine[i].get('to', ''), '4', dpr.daily_routine[i].get('duration', ''), '6', dpr.daily_routine[i].get('category', ''), '8', dpr.daily_routine[i].get('target_id', ''), '10', wrap_(dpr.daily_routine[i].get('description', ''), 16*2), '12', '13', '14'])
        group6_style.add('SPAN', (0, i+2), (1, i+2))
        group6_style.add('SPAN', (2, i+2), (3, i+2))
        group6_style.add('SPAN', (4, i+2), (5, i+2))
        group6_style.add('SPAN', (6, i+2), (7, i+2))
        group6_style.add('SPAN', (8, i+2), (9, i+2))
        group6_style.add('SPAN', (10, i+2), (13, i+2))
    
    group6_len_pre_extension = len(group6_data)

    group6_data.append(['Vessel', '2', wrap_('Total Number of Targets', 14), '4', wrap_('Total Number of Cleared Targets', 14), '6', wrap_('Number of Remaining Targets', 14), '8', wrap_('Total UXOs Found', 14), '10', wrap_('Targets Cleared Today', 14), '12', wrap_('Remarks', 14*2), '14'])
    group6_data.append([dpr.routine_vessel, '2', dpr.routine_total_targets, '4', dpr.routine_cleared_targets, '6', dpr.routine_remaining_targets, '8', dpr.routine_total_uxos_found, '10', dpr.routine_targets_cleared_today, '12', dpr.routine_remarks, '14'])

    group6_style.add('BACKGROUND', (0, group6_len_pre_extension), (13, group6_len_pre_extension), light_blue)

    for i in range(group6_len_pre_extension, len(group6_data)):
        group6_style.add('SPAN', (0, i), (1, i))
        group6_style.add('SPAN', (2, i), (3, i))
        group6_style.add('SPAN', (4, i), (5, i))
        group6_style.add('SPAN', (6, i), (7, i))
        group6_style.add('SPAN', (8, i), (9, i))
        group6_style.add('SPAN', (10, i), (11, i))
        group6_style.add('SPAN', (12, i), (13, i))

    group6_table = Table(group6_data, colWidths=[14*mm]*14)
    group6_table.setStyle(group6_style)

    elements.append(KeepTogether(group6_table))
    elements.append(Spacer(1, 15))

    previous = dpr.latest_dpr()

    group7_data = [
        ['I. Time Analysis Summary (hh:mm)', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        [wrap_('Category', 10), wrap_('Mob and Demob Survey Spread', 10), wrap_('Transit Time', 10), wrap_('Survey Spread Operational', 10), wrap_('Client Standby*', 10), wrap_('Weather Downtime', 10), wrap_('Time Based Work', 10), wrap_('Crew Change', 10), wrap_('Technical Downtime', 10), wrap_('Total', 10)],
        ['1', 'MOB', 'T', 'I', 'CS', 'WDT', 'TBW', 'CC', 'TDT', '10'],
        ['Previous', previous.mob_duration, previous.t_duration, previous.i_duration, previous.cs_duration, previous.wdt_duration, previous.tbw_duration, previous.cc_duration, previous.tdt_duration, previous.total_duration],
        ['Today', dpr.mob_duration, dpr.t_duration, dpr.i_duration, dpr.cs_duration, dpr.wdt_duration, dpr.tbw_duration, dpr.cc_duration, dpr.tdt_duration, dpr.total_duration],
        ['To Date', dpr.mob_duration_total, dpr.t_duration_total, dpr.i_duration_total, dpr.cs_duration_total, dpr.wdt_duration_total, dpr.tbw_duration_total, dpr.cc_duration_total, dpr.tdt_duration_total, dpr.total_duration_total],
        ['Notes: CS - any standby at direction of the client i.e. waiting on directions from the client']
    ]

    group7_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (9, 0)),
        ('SPAN', (0, 1), (0, 2)),
        ('SPAN', (9, 1), (9, 2)),
        ('BACKGROUND', (0, 0), (9, 0), dark_blue),
        ('BACKGROUND', (0, 1), (9, 2), light_blue),
    ])
    for i in range(1, 6):
        if i > 2:
            group7_style.add('SPAN', (0, i), (0, i))
        group7_style.add('SPAN', (1, i), (1, i))
        group7_style.add('SPAN', (2, i), (2, i))
        group7_style.add('SPAN', (3, i), (3, i))
        group7_style.add('SPAN', (4, i), (4, i))
        group7_style.add('SPAN', (5, i), (5, i))
        group7_style.add('SPAN', (6, i), (6, i))
        group7_style.add('SPAN', (7, i), (7, i))
        group7_style.add('SPAN', (8, i), (8, i))
        if i > 2:
            group7_style.add('SPAN', (9, i), (9, i))
    group7_style.add('SPAN', (0, 6), (9, 6))

    group7_table = Table(group7_data, colWidths=[20*mm]*10)
    group7_table.setStyle(group7_style)

    elements.append(KeepTogether(group7_table))
    elements.append(Spacer(1, 15))

    group8_data = [
        ['J. Minutes of Meeting', '2'],
        ['Interpreation of Weather Forecast (next 24 hours)', 'Technical Issues'],
        [wrap_(dpr.weather_interpretation, 100), wrap_(dpr.technical_issues, 100)],
        ['Meetings', 'Other'],
        [wrap_(dpr.meetings, 100), wrap_(dpr.other_remarks, 100)],
    ]

    group8_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 1), (0, 1)), ('SPAN', (1, 1), (1, 1)),
        ('SPAN', (0, 2), (0, 2)), ('SPAN', (1, 2), (1, 2)),
        ('SPAN', (0, 3), (0, 3)), ('SPAN', (1, 3), (1, 3)),
        ('SPAN', (0, 4), (0, 4)), ('SPAN', (1, 4), (1, 4)),
        ('BACKGROUND', (0, 0), (1, 0), dark_blue),
        ('BACKGROUND', (0, 1), (1, 1), light_blue),
        ('BACKGROUND', (0, 3), (1, 3), light_blue),
    ])

    group8_table = Table(group8_data, colWidths=[100*mm]*2)
    group8_table.setStyle(group8_style)

    elements.append(KeepTogether(group8_table))
    elements.append(Spacer(1, 15))

    group9_data = [
        ['K. Comments'],
        ['Client Comments'],
        [wrap_(dpr.client_comments, 125)],
        ['SeaTerra Comments'],
        [wrap_(dpr.seaterra_comments, 125)]
    ]

    group9_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, 0), dark_blue),
        ('BACKGROUND', (0, 1), (0, 1), light_blue),
        ('BACKGROUND', (0, 3), (0, 3), light_blue),
    ])

    group9_table = Table(group9_data, colWidths=[200*mm])
    group9_table.setStyle(group9_style)

    elements.append(KeepTogether(group9_table))
    elements.append(Spacer(1, 15))

    group10_data = [
        ['L. Signatures', '', '', ''],
        ['Client Amprion', '', 'OCM SeaTerra', '4'],
        ['Client name', format_ddmmyyyy(dpr.date), 'OCM name', format_ddmmyyyy(dpr.date)],
        ['', '', '', ''],
    ]

    group10_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (3, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)),
        ('SPAN', (0, 2), (0, 2)), ('SPAN', (1, 2), (1, 2)), ('SPAN', (2, 2), (2, 2)), ('SPAN', (3, 2), (3, 2)),
        ('SPAN', (0, 3), (1, 3)), ('SPAN', (2, 3), (3, 3)),
        ('BACKGROUND', (0, 0), (3, 0), dark_blue),
        ('BACKGROUND', (0, 1), (3, 1), light_blue),
    ])


    group10_table = Table(group10_data, colWidths=[50*mm]*4)
    group10_table.setStyle(group10_style)

    elements.append(KeepTogether(group10_table))
    elements.append(Spacer(1, 15))

    doc.build(elements)

    with open(file_path, 'rb') as f:
        pdf_bytes = f.read()
        f.close()
    os.remove(file_path)

    return HttpResponse(pdf_bytes, content_type='application/pdf')