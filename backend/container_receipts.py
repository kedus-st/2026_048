from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

from datetime import datetime

from clearance_app.models import MtlItem
from django.db.models import Count, Sum, Q

from django.core.files import File
import os

from textwrap import wrap

from clearance import settings

def create_wsc_receipt(wsc):

    file_path = f"tmp/{wsc.wsc_id}_record.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    image_seaterra_logo = Image(os.path.join(settings.IMAGES_ROOT, 'seaterra_logo.png'))
    image_seaterra_logo.drawWidth = 22 * mm
    image_seaterra_logo.drawHeight = 15 * mm

    items = MtlItem.objects.filter(wetstore_container=wsc)

    if wsc.eod:
        eod = wsc.eod
    else:
        eod = ''
    if wsc.closing_date:
        closing_date = wsc.closing_date.strftime('%d.%m.%Y')
    else:
        closing_date = ''
    if wsc.type == 'G':
        size = '1,'
    elif wsc.type == 'S':
        size = '0.5,'
    else:
        size = ''
    
    if wsc.wetstore_cell:
        cell = wsc.wetstore_cell.ws_cell_id
    else:
        cell = ''

    data = [
            #HEADER
            [os.environ['field_01'], '1', '2', '3', '4', '5', '6', '7', os.environ['field_02'], '9', '10', '11', '12',
             "\n".join(wrap("Nasslagerbehälter-Bericht / Wet Storage Container Record", 32)), '14', '15',
             '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            ["\n".join(wrap(os.environ['field_05'], 32)), '1', '2', '3', '4', '5', '6', '7', image_seaterra_logo, '9', '10',
             '11', '12', '13', '14', '15', '', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '', '14', '15', '16', '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', wsc.wsc_id, '14', '15',
             '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_09'], '1', '2', '3', "\n".join(wrap(os.environ['field_10'], 35)), '5', '6', '7', '8', '9', '10', '11', '12',
             os.environ['field_11'], '14', '15', '16', os.environ['field_11'], '18', "\n".join(wrap(os.environ['field_12'], 30)), '20', '21', '22', '23', '24', '25'],
            [os.environ['field_13'], '1', '2', '3', "Pelzerhaken", '5', '6', '7', '8', '9',
             '10', '11', '12', os.environ['field_16'], '14', '15', '16', '17', '18', "\n".join(wrap(os.environ['field_17'], 20)), '20', '21', '22', '23', '24', '25'],
            
            #GENERAL INFO
            ["NASSLAGERDOKUMENTATION / WET STORAGE DOCUMENTATION", '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
             '16',
             '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],
            ['Truppführer §20 SprengG\nEOD Supervisor:', '1', '2', '3', '4', '5', '6', eod, '8', '9', '10', '11', '12', "\n".join(wrap('Räumschiff\n clearance vessel:',20)), '14', '15', 'NP 562', '17',
             "\n".join(wrap('Datum Lagerung/ date of storage  (ddmmyyyy)', 22)),
             '19', '20', '21', '22',  closing_date, '24', '25'],
            ["\n".join(wrap('Nettoexplosivmasse NEM\nnet explosive weight NEW [kg]:', 32)), '1', '2', '3', '4', '5', '6', int(wsc.total_ex_weight or 0), 'Größe Behälter (L, Ø)\nsize container [m]:', '9', '10', '11', size, "\n".join(wrap('Nasslager-Position\nwet storage position (ETRS89 / UTM32N)', 22)), '14', '15', '16', '17', 'E',
             wsc.easting, '20', '21', 'Wassertiefe\nwater depth [m]:', '23', '24', wsc.water_depth],
            ["\n".join(wrap('Gewicht Kampfmittel\nweight of UXO [kg]:', 32)), '1', '2', '3', '4', '5', '6', int(wsc.mtl_weight), 'Gesamtgewicht\nTotal Weight [kg]', '9', '10', '11', int(wsc.total_weight), '13', '14', '15', '16', '17', 'N',
             wsc.northing, '20', '21', 'Block\nblock:', '23', '24', cell],
            ['Beschreibung/ description: ', '1', '2', '3', '4', '5', '6', wsc.content_type, '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],
            ['Anmerkungen/ comments: ', '1', '2', '3', '4', '5', '6', wsc.record_comment, '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],

            #CONTENT INFO
            ["BESTÜCKUNG DES NASSLAGERBEHÄLTERS / CONTENT OF THE WET STORAGE CONTAINER", '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
             '16',
             '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],
    ]

    item_list = []

    for item in items:
        row1 = ['Kampfmittel / Ordnance ID', '1', '2', '3', '4', '5', '6', '7', item.identifier, '9', '10', '11', '12', "\n".join(wrap('KM-Kategorie /\n UXO Category',22)), '14', '15', '16', '17', '18',
             item.type,
             '20', '21', '22', '23', '24', '25']
        row2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', "\n".join(wrap('KM-Bezeichnung /\n UXO classification', 22)), '14', '15', '16', '17', '18',
             item.type_detail,
             '20', '21', '22', '23', '24', '25']
        
        item_list.append(row1)
        item_list.append(row2)

    data.extend(item_list)

    if eod.startswith('Tjerk Reichel'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/tjerk_reichelt_signature.jpg'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm
    elif eod.startswith('Andre Hartmann'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/andre_hartmann_signature.png'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 18 * mm
    elif eod.startswith('Frank Diestel'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/frank_diestel_signature.png'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 28 * mm
    elif eod.startswith('Martin Kano'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/martin_kano_signature.jpg'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 16 * mm
    elif eod.startswith('Stefan Fiedler'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 28 * mm
    elif eod.startswith('Dragan Mirjanic'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/dragan_mirjanic_signature.jpg'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 28 * mm
    elif eod.startswith('Christian Richter'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/christian_richter_signature.jpg'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 16 * mm
    elif eod.startswith('Janusz Lemieszek'):
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/janusz_lemieszek_signature.jpg'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 16 * mm
    else:
        eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
        eod_signature.drawHeight = 8 * mm
        eod_signature.drawWidth = 28 * mm

    image_qa_signature_edgar_schwab = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
    image_qa_signature_edgar_schwab.drawHeight = 8 * mm
    image_qa_signature_edgar_schwab.drawWidth = 28 * mm

    date = datetime.now().strftime("%d.%m.%Y")

    signature_data = [
            ['UNTERSCHRIFTEN / SIGNATURES', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '', '14', '15',
             '16',
             '17',
             '18', '19', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_53'], '1', '2', date, '4', '5', eod_signature, '7', '8', '9', '10', '11', '12', os.environ['field_53'], '14', '15',
             date,
             '17',
             '18', image_qa_signature_edgar_schwab, '20', '21', '22', '23', '24', '25'],
            ["\n".join(wrap(os.environ['field_56'], 25)), '1', '2', '3', '4', '5', os.environ['field_55'], '7', '8', '9', '10', '11',
             '12',
             os.environ['field_58'], '14', '15', '16', '17', '18', os.environ['field_55'], '20', '21', '22', '23', '24',
             '25'],
            ['', '1', '2', '3', '4', '5', os.environ['field_59'], '7', '8', eod, '10', '11', '12', '13', '14', '15',
             '16',
             '17',
             '18',
             os.environ['field_59'], '20', '21', os.environ['field_60'], '23', '24', '25'],
    ]

    data.extend(signature_data)

    style = TableStyle([
            #HEADER
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('SPAN', (0, 0), (7, 0)), ('SPAN', (8, 0), (12, 0)), ('SPAN', (13, 0), (25, 2)),
            ('FONTSIZE', (0, 0), (7, 0), 7), ('FONTSIZE', (8, 0), (12, 0), 6), ('FONTSIZE', (13, 0), (25, 2), 16),
            ('FONTNAME', (13, 0), (25, 2), 'Helvetica-Bold'),
            ('BACKGROUND', (13, 0), (25, 2), '#DAE3F3'),

            ('SPAN', (0, 1), (7, 4)), ('SPAN', (8, 1), (12, 4)),
            ('SPAN', (13, 3), (25, 4)),
            ('FONTSIZE', (3, 1), (7, 4), 10), ('FONTSIZE', (13, 3), (15, 4), 16), ('FONTSIZE', (16, 3), (25, 4), 16),
            ('FONTNAME', (13, 3), (15, 4), 'Helvetica-Bold'), ('FONTNAME', (16, 3), (25, 4), 'Helvetica-Bold'),
            ('BACKGROUND', (13, 3), (25, 4), '#DAE3F3'),
            ('VALIGN', (13, 3), (25, 4), 'TOP'),

            ('SPAN', (0, 5), (3, 5)), ('SPAN', (4, 5), (12, 5)), ('SPAN', (13, 5), (18, 5)),
            ('FONTSIZE', (4, 5), (12, 5), 10),
            #('LEADING', (4, 5), (12, 5), 8),
            ('SPAN', (19, 5), (25, 5)),
            ('FONTSIZE', (19, 5), (25, 5), 9),
            ('ALIGN', (0, 5), (3, 5), 'LEFT'), ('ALIGN', (13, 5), (18, 5), 'LEFT'),
            ('BACKGROUND', (0, 5), (3, 5), '#F2F2F2'),

            ('SPAN', (0, 6), (3, 6)), ('SPAN', (4, 6), (12, 6)),
            ('SPAN', (13, 6), (18, 6)),
            ('SPAN', (19, 6), (25, 6)),
            ('ALIGN', (0, 6), (25, 6), 'LEFT'),
            ('ALIGN', (6, 6), (12, 6), 'CENTER'),
            ('BACKGROUND', (0, 6), (3, 6), '#F2F2F2'),

            #GENERAL INFO
            ('SPAN', (0, 7), (25, 7)),
            ('ALIGN', (0, 7), (25, 7), 'LEFT'),
            ('FONTSIZE', (0, 7), (25, 7), 10),
            ('FONTNAME', (0, 7), (25, 7), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 7), (25, 7), '#DAE3F3'),

            ('SPAN', (0, 8), (6, 8)), ('SPAN', (7, 8), (12, 8)), ('SPAN', (13, 8), (15, 8)), ('SPAN', (16, 8), (17, 8)), ('SPAN', (18, 8), (22, 8)), ('SPAN', (23, 8), (25, 8)),
            ('SPAN', (0, 9), (6, 9)), ('SPAN', (7, 9), (7, 9)), ('SPAN', (8, 9), (11, 9)), ('SPAN', (12, 9), (12, 9)), ('SPAN', (18, 9), (18, 9)), ('SPAN', (19, 9), (21, 9)), ('SPAN', (22, 9), (24, 9)), ('SPAN', (25, 9), (25, 9)),
            ('SPAN', (0, 10), (6, 10)), ('SPAN', (7, 10), (7, 10)), ('SPAN', (8, 10), (11, 10)), ('SPAN', (12, 10), (12, 10)), ('SPAN', (13, 9), (17, 10)), ('SPAN', (18, 10), (18, 10)), ('SPAN', (19, 10), (21, 10)), ('SPAN', (22, 10), (24, 10)), ('SPAN', (25, 10), (25, 10)),
            ('SPAN', (0, 11), (6, 11)), ('SPAN', (7, 11), (25, 11)),
            ('SPAN', (0, 12), (6, 12)), ('SPAN', (7, 12), (25, 12)),
            ('FONTSIZE', (0, 8), (25, 12), 8),

            ('BACKGROUND', (0, 8), (6, 8), '#F2F2F2'), ('BACKGROUND', (13, 8), (15, 8), '#F2F2F2'), ('BACKGROUND', (18, 8), (22, 8), '#F2F2F2'),
            ('BACKGROUND', (0, 9), (6, 9), '#F2F2F2'), ('BACKGROUND', (8, 9), (11, 9), '#F2F2F2'), ('BACKGROUND', (13, 9), (17, 10), '#F2F2F2'), ('BACKGROUND', (22, 9), (24, 9), '#F2F2F2'),
            ('BACKGROUND', (0, 10), (6, 10), '#F2F2F2'), ('BACKGROUND', (8, 10), (11, 10), '#F2F2F2'), ('BACKGROUND', (22, 10), (24, 10), '#F2F2F2'),
            ('BACKGROUND', (0, 11), (6, 11), '#F2F2F2'),
            ('BACKGROUND', (0, 12), (6, 12), '#F2F2F2'),
            ('ALIGN', (7, 11), (25, 11), 'LEFT'),
            ('ALIGN', (7, 12), (25, 12), 'LEFT'),

            #CONTENT INFO
            ('SPAN', (0, 13), (25, 13)),
            ('ALIGN', (0, 13), (25, 13), 'LEFT'),
            ('FONTSIZE', (0, 13), (25, 13), 10),
            ('FONTNAME', (0, 13), (25, 13), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 13), (25, 13), '#DAE3F3'),

        ])
    
    row_index = 0

    for i in range(len(items)):
        row_index = 14 + i*2
        spans = [
            ('SPAN', (0, row_index), (7, row_index+1)),
            ('SPAN', (8, row_index), (12, row_index+1)),
            ('SPAN', (13, row_index), (18, row_index)),
            ('SPAN', (13, row_index+1), (18, row_index+1)),
            ('SPAN', (19, row_index), (25, row_index)),
            ('SPAN', (19, row_index+1), (25, row_index+1)),
        ]
        for span in spans:
            style.add(*span)

    signature_spans = [
        ('SPAN', (0, row_index+2), (25, row_index+2)),
        ('ALIGN', (0, row_index+2), (25, row_index+2), 'LEFT'),
        ('FONTSIZE', (0, row_index+2), (25, row_index+2), 10),
        ('FONTNAME', (0, row_index+2), (25, row_index+2), 'Helvetica-Bold'),
        ('BACKGROUND', (0, row_index+2), (25, row_index+2), '#DAE3F3'),

        ('SPAN', (0, row_index+3), (2, row_index+3)), ('SPAN', (3, row_index+3), (5, row_index+3)), ('SPAN', (6, row_index+3), (12, row_index+3)), ('SPAN', (13, row_index+3), (15, row_index+3)), ('SPAN', (16, row_index+3), (18, row_index+3)), ('SPAN', (19, row_index+3), (25, row_index+3)),
        ('SPAN', (0, row_index+4), (5, row_index+5)), ('SPAN', (6, row_index+4), (12, row_index+4)), ('SPAN', (13, row_index+4), (18, row_index+5)), ('SPAN', (19, row_index+4), (25, row_index+4)),
        ('VALIGN', (0, row_index+4), (5, row_index+5), 'TOP'),
        ('SPAN', (0, row_index+5), (5, row_index+5)), ('SPAN', (6, row_index+5), (8, row_index+5)), ('SPAN', (9, row_index+5), (12, row_index+5)), ('SPAN', (19, row_index+5), (21, row_index+5)), ('SPAN', (22, row_index+5), (25, row_index+5)),
    ]

    for span in signature_spans:
        style.add(*span)
    
    row_heights = [
        #HEADER
        4.5 * mm,
        4.5 * mm,
        4.5 * mm,
        4.5 * mm,
        4.5 * mm,
        16 * mm,
        9 * mm,

        #GENERAL INFO
        8 * mm,
        9 * mm,
        9 * mm,
        9 * mm,
        9 * mm,
        9 * mm,

        #CONTENT INFO
        8 * mm,

    ]

    for item in items:
        row_heights.append(9 * mm)
        row_heights.append(9 * mm)

    row_heights.append(8*mm)
    row_heights.append(10*mm)
    row_heights.append(6*mm)
    row_heights.append(6*mm)

    t = Table(data, colWidths=7.5 * mm, rowHeights=row_heights)

    t.setStyle(style)
    elements.append(t)
    doc.build(elements)

    with open(file_path, 'rb') as file:
        file_data = File(file)
        wsc.document.save(f"{wsc.wsc_id}_record.pdf", file_data)

    os.remove(file_path)

def create_wsc_receipt_old(wsc):

    file_path = f"tmp/{wsc.wsc_id}_receipt.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    
    left_paragraphs = [
        Paragraph(f"Firma: SeaTerra GmbH", styles["Normal"]),
        Paragraph(f"Räumstelle / Bauvorhaben: Sofortprogramm / Los 3- Pelzerhaken", styles["Normal"]),
        Paragraph(f"Auftrags-Nummer: LBA-2024-1406", styles["Normal"]),
        Paragraph(f"StandKatalog: 01.07.2020", styles["Normal"])
    ]

    right_paragraphs = [
        Paragraph(f"Nasslagerbehälter " + str(wsc.wsc_id), styles["Normal"]),
        Paragraph(f"Behälter Art: " + str(wsc.type), styles["Normal"]),
        Paragraph(f"Nasslager Zelle " + str(wsc.wetstore_cell) if wsc.wetstore_cell else "", styles["Normal"]),
        Paragraph(f"Datum: " + str(datetime.now().date()), styles["Normal"]),
        #Paragraph(f"Räumungszeitraum von:  bis: ", styles["Normal"]),
        #Paragraph(f"StandKatalog: ", styles["Normal"])
    ]

    info_data = [[left_paragraphs, right_paragraphs]]

    info_table = Table(info_data, colWidths=[120*mm, 50*mm])

    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 24))

    table_data = [
        ["Anzahl", "1", "Masse", "3", "Munition", "5", "6", "7", "Zuordnung", "9", "Einzelgewicht",    "11", "12",  "13", "Gesamtgewicht",  "15",   "16", "17"],
        ["Stück",  "1",  "kg",   "3",       "",   "5", "6", "7",  "",         "9", "brutto",           "11","NEM",  "13", "brutto",         "15",   "NEM", "17"],
    ]

    items = MtlItem.objects.filter(wetstore_container=wsc)
    distinct_counts = items.values('country', 'type').annotate(
        count=Count('id'),
        total_weight=Sum('cl_weight'),
        total_explosive_weight=Sum('explosive_weight')
    ).order_by()

    item_list = []

    for entry in distinct_counts:
        mass = ""
        count = entry['count']
        type = entry['type']
        country = entry['country']
        total_weight = entry['total_weight'] or 0
        nem = entry['total_explosive_weight'] or 0

        row = [count, "1", mass, "3", "\n".join(wrap(type, 20)), "5", "6", "7", "\n".join(wrap(country, 10)), "9", round(total_weight/count, 2), "11", round(nem/count,2), "13", total_weight, "15", nem]
    
        item_list.append(row)
    
    table_data.extend(item_list)
    table = Table(table_data, colWidths=10*mm, rowHeights=12*mm)
    table_style = TableStyle([
        ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)), ('SPAN', (4, 0), (7, 0)), ('SPAN', (8, 0), (9, 0)), ('SPAN', (10, 0), (13, 0)), ('SPAN', (14, 0), (17, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (7, 1)), ('SPAN', (8, 1), (9, 1)), ('SPAN', (10, 1), (11, 1)), ('SPAN', (12, 1), (13, 1)), ('SPAN', (14, 1), (15, 1)), ('SPAN', (16, 1), (17, 1)),
        
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ])
    num_types = len(item_list)
    for i in range(num_types):
        row_index = 2 + i
        spans = [
            ('SPAN', (0, row_index), (1, row_index)),
            ('SPAN', (2, row_index), (3, row_index)),
            ('SPAN', (4, row_index), (7, row_index)),
            ('SPAN', (8, row_index), (9, row_index)),
            ('SPAN', (10, row_index), (11, row_index)),
            ('SPAN', (12, row_index), (13, row_index)),
            ('SPAN', (14, row_index), (15, row_index)),
            ('SPAN', (16, row_index), (17, row_index)),
        ]
        for span in spans:
            table_style.add(*span)

    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 24))

    summary_table_data = [
        ["Zusammenfassung", "", "", "", "", "", "", ""],
        ["Anzahl Stück", "1", "Masse kg",  "3", "Brutto kg",  "5", "NEM kg"],
        [wsc.mtl_items_count, "1", "", "3", wsc.total_weight-wsc.container_weight, "5", wsc.total_ex_weight]
    ]

    summary_table = Table(summary_table_data, colWidths=22.5*mm)
    summary_table_style = TableStyle([
        ('SPAN', (0, 0), (7, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)),
        ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (3, 2)), ('SPAN', (4, 2), (5, 2)), ('SPAN', (6, 2), (7, 2)),

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    summary_table.setStyle(summary_table_style)
    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    total_mass = items.aggregate(total_mass=Sum('cl_weight'))['total_mass']

    german_mass = items.filter(
        Q(country__iexact='DE') |
        Q(country__icontains='Deutsch') |
        Q(country__icontains='Germany')
    ).aggregate(german_mass=Sum('cl_weight'))['german_mass']

    origin_table_data = [
        ["", "1", "Zuordnung", "3", "Prozentanteil", "5", "Masse", ""],
        ["Anteil Munition", "1", "Deutsch",  "3", round(100*german_mass/total_mass, 2),  "5", german_mass],
        ["Anteil Munition", "1", "Andere",  "3", round(100*(total_mass-german_mass)/total_mass, 2),  "5", total_mass-german_mass],
    ]

    origin_table = Table(origin_table_data, colWidths=22.5*mm)
    origin_table_style = TableStyle([
        ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)), ('SPAN', (4, 0), (5, 0)), ('SPAN', (6, 0), (7, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)),
        ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (3, 2)), ('SPAN', (4, 2), (5, 2)), ('SPAN', (6, 2), (7, 2)),

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    origin_table.setStyle(origin_table_style)
    elements.append(origin_table)
    elements.append(Spacer(1, 24))

    signatures_table_data = [
        ["Unterschriften", "", "", "", "", "", "", ""],
        ["Übergeben an \nTransportschiff\n(§20 Feuerwerker)", "1", "",  "3", "Abgelegt auf UW Position\n(§20 Feuerwerker)",  "5", ""],
    ]

    signatures_table = Table(signatures_table_data, colWidths=23*mm, rowHeights=[5*mm, 20*mm])
    signatures_table_style = TableStyle([
        ('SPAN', (0, 0), (7, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)),

        ('VALIGN', (0, 1), (1, 1), 'TOP'), ('VALIGN', (4, 1), (5, 1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    signatures_table.setStyle(signatures_table_style)
    elements.append(signatures_table)
    elements.append(Spacer(1, 24))

    doc.build(elements)

    with open(file_path, 'rb') as file:
        file_data = File(file)
        wsc.document.save(f"{wsc.wsc_id}_receipt.pdf", file_data)

    os.remove(file_path)

def create_hoc_receipt(hoc):

    file_path = f"tmp/{hoc.hoc_id}_receipt.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
    
    left_paragraphs = [
        Paragraph(f"Firma: SeaTerra GmbH", styles["Normal"]),
        Paragraph(f"Räumstelle / Bauvorhaben: Sofortprogramm / Los 3- Pelzerhaken", styles["Normal"]),
        Paragraph(f"Auftrags-Nummer: LBA-2024-1406", styles["Normal"]),
        Paragraph(f"StandKatalog: 01.07.2020", styles["Normal"])
    ]

    right_paragraphs = [
        Paragraph(f"Übergabebehälter " + str(hoc.hoc_id), styles["Normal"]),
        Paragraph(f"Datum: " + str(datetime.now().date()), styles["Normal"]),
        #Paragraph(f"Räumungszeitraum von:  bis: ", styles["Normal"]),
        #Paragraph(f"StandKatalog: ", styles["Normal"])
    ]

    info_data = [[left_paragraphs, right_paragraphs]]

    info_table = Table(info_data, colWidths=[120*mm, 50*mm])

    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 24))

    table_data = [
        ["Anzahl", "1", "Masse", "3", "Munition", "5", "6", "7", "Zuordnung", "9", "Einzelgewicht",    "11", "12",  "13", "Gesamtgewicht",  "15",   "16", "17"],
        ["Stück",  "1",  "kg",   "3",       "",   "5", "6", "7",  "",         "9", "brutto",           "11","NEM",  "13", "brutto",         "15",   "NEM", "17"],
    ]

    items = MtlItem.objects.filter(handover_container=hoc)
    distinct_counts = items.values('country', 'type').annotate(
        count=Count('id'),
        total_weight=Sum('cl_weight'),
        total_explosive_weight=Sum('explosive_weight')
    ).order_by()

    item_list = []

    for entry in distinct_counts:
        mass = ""
        count = entry['count']
        type = entry['type']
        country = entry['country']
        total_weight = entry['total_weight'] or 0
        nem = entry['total_explosive_weight'] or 0

        row = [count, "1", mass, "3", "\n".join(wrap(type, 20)), "5", "6", "7", "\n".join(wrap(country, 10)), "9", round(total_weight/count,2), "11", round(nem/count,2), "13", total_weight, "15", nem]
    
        item_list.append(row)
    
    table_data.extend(item_list)
    table = Table(table_data, colWidths=10*mm, rowHeights=12*mm)
    table_style = TableStyle([
        ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)), ('SPAN', (4, 0), (7, 0)), ('SPAN', (8, 0), (9, 0)), ('SPAN', (10, 0), (13, 0)), ('SPAN', (14, 0), (17, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (7, 1)), ('SPAN', (8, 1), (9, 1)), ('SPAN', (10, 1), (11, 1)), ('SPAN', (12, 1), (13, 1)), ('SPAN', (14, 1), (15, 1)), ('SPAN', (16, 1), (17, 1)),
        
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ])
    num_types = len(item_list)
    for i in range(num_types):
        row_index = 2 + i
        spans = [
            ('SPAN', (0, row_index), (1, row_index)),
            ('SPAN', (2, row_index), (3, row_index)),
            ('SPAN', (4, row_index), (7, row_index)),
            ('SPAN', (8, row_index), (9, row_index)),
            ('SPAN', (10, row_index), (11, row_index)),
            ('SPAN', (12, row_index), (13, row_index)),
            ('SPAN', (14, row_index), (15, row_index)),
            ('SPAN', (16, row_index), (17, row_index)),
        ]
        for span in spans:
            table_style.add(*span)

    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 24))

    summary_table_data = [
        ["Zusammenfassung", "", "", "", "", "", "", ""],
        ["Anzahl Stück", "1", "Masse kg",  "3", "Brutto kg",  "5", "NEM kg"],
        [hoc.mtl_items_count, "1", "", "3", hoc.total_weight, "5", hoc.total_ex_weight]
    ]

    summary_table = Table(summary_table_data, colWidths=22.5*mm)
    summary_table_style = TableStyle([
        ('SPAN', (0, 0), (7, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)),
        ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (3, 2)), ('SPAN', (4, 2), (5, 2)), ('SPAN', (6, 2), (7, 2)),

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    summary_table.setStyle(summary_table_style)
    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    total_mass = items.aggregate(total_mass=Sum('cl_weight'))['total_mass']

    german_mass = items.filter(
        Q(country__iexact='DE') |
        Q(country__icontains='Deutsch') |
        Q(country__icontains='Germany')
    ).aggregate(german_mass=Sum('cl_weight'))['german_mass']

    origin_table_data = [
        ["", "1", "Zuordnung", "3", "Prozentanteil", "5", "Masse", ""],
        ["Anteil Munition", "1", "Deutsch",  "3", round(100*german_mass/total_mass, 2),  "5", german_mass],
        ["Anteil Munition", "1", "Andere",  "3", round(100*(total_mass-german_mass)/total_mass, 2),  "5", total_mass-german_mass],
    ]

    origin_table = Table(origin_table_data, colWidths=22.5*mm)
    origin_table_style = TableStyle([
        ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)), ('SPAN', (4, 0), (5, 0)), ('SPAN', (6, 0), (7, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)),
        ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (3, 2)), ('SPAN', (4, 2), (5, 2)), ('SPAN', (6, 2), (7, 2)),

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    origin_table.setStyle(origin_table_style)
    elements.append(origin_table)
    elements.append(Spacer(1, 24))

    signatures_table_data = [
        ["Unterschriften", "", "", "", "", "", "", ""],
        ["Übergeben:\n(§20 Feuerwerker)", "1", "",  "3", "Übernommen:\n(Kampfmittelräumdienst S-H)",  "5", ""],
    ]

    signatures_table = Table(signatures_table_data, colWidths=23*mm, rowHeights=[5*mm, 40*mm])
    signatures_table_style = TableStyle([
        ('SPAN', (0, 0), (7, 0)),
        ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)), ('SPAN', (4, 1), (5, 1)), ('SPAN', (6, 1), (7, 1)),

        ('VALIGN', (0, 1), (1, 1), 'TOP'), ('VALIGN', (4, 1), (5, 1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    signatures_table.setStyle(signatures_table_style)
    elements.append(signatures_table)
    elements.append(Spacer(1, 24))

    doc.build(elements)
    
    with open(file_path, 'rb') as file:
        file_data = File(file)
        hoc.document.save(f"{hoc.hoc_id}_receipt.pdf", file_data)

    os.remove(file_path)