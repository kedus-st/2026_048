import os, datetime
from backend.blob_actions import list_blobs, overwrite_tr, save_pdf, get_secure_blob_url

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Image, SimpleDocTemplate
from textwrap import wrap

from clearance import settings

from PIL import Image as PILImage
import requests
from io import BytesIO

from clearance_app.models import MtlItemImage

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

def register_fonts():
    base = os.path.join(settings.STATIC_ROOT, 'fonts')  # adjust to where your .ttf files live
    pdfmetrics.registerFont(TTFont('Arimo',            os.path.join(base, 'Arimo-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Arimo-Bold',       os.path.join(base, 'Arimo-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('Arimo-Italic',     os.path.join(base, 'Arimo-Italic.ttf')))
    pdfmetrics.registerFont(TTFont('Arimo-BoldItalic', os.path.join(base, 'Arimo-BoldItalic.ttf')))

    addMapping('Arimo', 0, 0, 'Arimo')
    addMapping('Arimo', 1, 0, 'Arimo-Bold')
    addMapping('Arimo', 0, 1, 'Arimo-Italic')
    addMapping('Arimo', 1, 1, 'Arimo-BoldItalic')

def create_tr(mtl_item):
        print("Starting recreation")
        #query = self.__class__.objects.get(itp_no_mag=itp_no_mag)
        query = mtl_item

        itp_no_mag = query.itp_no_mag

        overwrite_tr(str(itp_no_mag))

        #if(None in [query.clear, query.found, query.eod] or '' in [query.clear, query.found, query.eod]):
        #    return
        if query.clear is None or query.qa_clear is None:
            return
        if ('y' not in query.qa_clear or 'y' not in query.clear):
            return
        value_08 = itp_no_mag
        value_20 = query.eod
        value_22 = query.cl_date
        if value_22 is not None:
            value_22 = value_22.strftime("%d.%m.%Y")
        else:
            value_22 = ''
        value_25a = query.found
        if value_25a and 'y' in value_25a:
            value_25a = 'Y'
        else:
            value_25a = 'N'
        value_27 = query.cl_weight
        value_29 = query.cl_depth_bg

        # Avoid 'None', make empty instead
        value_31 = (str(query.cl_length) + '/\n' + str(query.cl_width)).replace('None/\nNone', '')

        value_33 = query.clear
        if value_33 and 'y' in value_33:
            value_33 = 'Y'
        else:
            value_33 = 'N'
        value_36 = query.easting
        value_40 = query.northing
        value_42 = query.description_detail
        if value_42 == None:
            value_42 = ''
        value_43a_string = query.tr_comment
        value_43a = ''
        if query.tr_comment is not None:
            if len(query.tr_comment) > 122:
                # value_43a = value_43a_string[:121] + '\n' + value_43a_string[121:]
                value_43a = value_43a_string.replace('\\n', '\n')
            else:
                value_43a = value_43a_string
        else:
            value_43a = ''

        value_54 = datetime.datetime.now().strftime("%Y%m%d-%H%M")

        mtlimages = list_blobs('media/mtlimages/')
        magimages = list_blobs('media/magimages/')
        sssimages = list_blobs('media/sssimages/')
        mbesimages = list_blobs('media/mbesimages/')
        topoimages = list_blobs('media/topoimages/')
        # image_itp = Image(os.path.join(settings.ITP_IMAGES_ROOT, 'MTL-1401_pic_1.JPG'))

        images = list(MtlItemImage.objects.filter(mtl_item__itp_no_mag=itp_no_mag))
        if images:
            if images[0].mtl_item_image.name:
                image_itp1 = Image(get_secure_blob_url(images[0].mtl_item_image.name))
                image_itp1.drawHeight = 53 * mm
                image_itp1.drawWidth = 74 * mm
            else:
                image_itp1 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
                image_itp1.drawHeight = 53 * mm
                image_itp1.drawWidth = 74 * mm
            if len(images) > 1:
                if images[1].mtl_item_image.name:
                    image_itp2 = Image(get_secure_blob_url(images[1].mtl_item_image.name))
                    image_itp2.drawHeight = 53 * mm
                    image_itp2.drawWidth = 74 * mm
                else:
                    image_itp2 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
                    image_itp2.drawHeight = 53 * mm
                    image_itp2.drawWidth = 74 * mm
            else:
                image_itp2 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
                image_itp2.drawHeight = 53 * mm
                image_itp2.drawWidth = 74 * mm
        else:
            image_itp1 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_itp1.drawHeight = 53 * mm
            image_itp1.drawWidth = 74 * mm

            image_itp2 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_itp2.drawHeight = 53 * mm
            image_itp2.drawWidth = 74 * mm

        if (settings.PROJECT_NAME+'/media/magimages/'+str(itp_no_mag) + '_TMI_IMAGE.png' in magimages):      
            image_tmi = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/magimages/'+str(itp_no_mag) + '_TMI_IMAGE.png'))
            image_tmi.drawHeight = 40 * mm
            image_tmi.drawWidth = 80 * mm
        else:
            image_tmi = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_tmi.drawHeight = 53 * mm
            image_tmi.drawWidth = 74 * mm

        if (settings.PROJECT_NAME+'/media/topoimages/'+str(itp_no_mag) + '_TOPO_IMAGE.png' in topoimages):
            image_topo = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/topoimages/'+str(itp_no_mag) + '_TOPO_IMAGE.png'))
            image_topo.drawWidth = 80 * mm
            image_topo.drawHeight = 40 * mm
        else:
            image_topo = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_topo.drawHeight = 53 * mm
            image_topo.drawWidth = 53 * mm

        if False:#(settings.PROJECT_NAME+'/media/mbesimages/'+str(itp_no_mag) + '_MBES_IMAGE.png' in mbesimages):
            image_mbes = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/mbesimages/'+str(itp_no_mag) + '_MBES_IMAGE.png'))
            image_mbes.drawWidth = 53 * mm
            image_mbes.drawHeight = 53 * mm
        else:
            image_mbes = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_mbes.drawHeight = 53 * mm
            image_mbes.drawWidth = 74 * mm

        #if(settings.PROJECT_NAME+'/media/sssimages/'+str(itp_no_mag) + '_TOPO_IMAGE.png' in sssimages):
        #if(any(str(itp_no_mag) + '_TOPO_IMAGE.png' in imgs for imgs in topoimages):
        #try:
        #    image_sss = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/sssimages/'+str(itp_no_mag) + '_TOPO_IMAGE.png'))
        #    image_sss.drawWidth = 90 * mm
        #    image_sss.drawHeight = 45 * mm
        #else:
        #    image_sss = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
        #    image_sss.drawHeight = 53 * mm
        #    image_sss.drawWidth = 74 * mm
        
        #if(settings.PROJECT_NAME+'/media/mbesimages/'+str(itp_no_mag) + '_MBES_IMAGE.png' in mbesimages):
        #try:
        #    image_mbes = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/mbesimages/'+str(itp_no_mag) + '_MBES_IMAGE.png'))
        #    image_mbes.drawHeight = 45 * mm
        #    image_mbes.drawWidth = 90 * mm
        #else:
        #    image_mbes = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
        #    image_mbes.drawHeight = 53 * mm
        #    image_mbes.drawWidth = 74 * mm


        image_clinet_logo = Image(os.path.join(settings.IMAGES_ROOT, 'client_logo.png'))
        image_clinet_logo.drawWidth = 16 * mm
        image_clinet_logo.drawHeight = 8.5 * mm

        image_seaterra_logo = Image(os.path.join(settings.IMAGES_ROOT, 'seaterra_logo.png'))
        image_seaterra_logo.drawWidth = 17 * mm
        image_seaterra_logo.drawHeight = 12 * mm

        # EOD SIGNATURES

        value_20 = 'Janusz Lemieszek'

        if value_20.startswith('André Böhme'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/andre_boehme_signature.jpg'))
            eod_signature.drawHeight = 13 * mm
            eod_signature.drawWidth = 36 * mm
        elif value_20.startswith('Tjerk Reichel'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/tjerk_reichelt_signature.jpg'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm
        elif value_20.startswith('Andre Hartmann'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/andre_hartmann_signature.png'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 18 * mm
        elif value_20.startswith('Frank Diestel'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/frank_diestel_signature.png'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm
        elif value_20.startswith('Martin Kano'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/martin_kano_signature.jpg'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 16 * mm
        elif value_20.startswith('Stefan Fiedler'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm
        elif value_20.startswith('Dragan Mirjanic'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/dragan_mirjanic_signature.jpg'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm
        elif value_20.startswith('Christian Richter'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/christian_richter_signature.jpg'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 16 * mm
        elif value_20.startswith('Janusz Lemieszek'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/janusz_lemieszek_signature.jpg'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 16 * mm
        else:
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm

        image_qa_signature_edgar_schwab = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
        image_qa_signature_edgar_schwab.drawHeight = 13 * mm
        image_qa_signature_edgar_schwab.drawWidth = 36 * mm

        file_path = 'tmp/' + str(settings.TARGET_RECORD_PREFIX) + str(
            itp_no_mag) + '(' + value_54 + ').pdf'

        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm, topMargin=14 * mm,
                                bottomMargin=14 * mm)
        doc.pagesize = portrait(A4)
        elements = []

        # Vessel + fixed project clearance-depth value (constants for this template)
        value_20a = os.environ.get('field_20a', '')
        clearance_depth = '-5 m / -17.5 mNH'

        E = ''  # filler for cells hidden behind a SPAN

        # 25 columns (Excel B..Z), 21 rows (Excel 1..21)
        data = [
            # row 0 - contractor headers + title
            [os.environ['field_01'], E, E, E, E, E, E, E, os.environ['field_02'], E, E, E, E, E,
             os.environ['field_03'], E, E, E, E, E, E, E, E, E, E],
            # row 1 - client logo | address | seaterra logo | (title span)
            [image_clinet_logo, E, E, "\n".join(wrap(os.environ['field_05'], 26)), E, E, E, E,
             image_seaterra_logo, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
            # row 2 - MTL | target number
            [E, E, E, E, E, E, E, E, E, E, E, E, E, E,
             os.environ['field_07'], E, value_08, E, E, E, E, E, E, E, E],
            # row 3 - (all covered by spans above)
            [E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
            # row 4 - Project | description | General Contractor | value
            [os.environ['field_09'], E, E, "\n".join(wrap(os.environ['field_10'], 70)), E, E, E, E, E, E, E, E, E, E,
             os.environ['field_11'], E, E, E, E, E, E, E,
             "\n".join(wrap(os.environ['field_12'], 18)), E, E],
            # row 5 - Lokalizacja | value | Project Manager | value
            [os.environ['field_13'], E, E, os.environ['field_14'], E, E, E, E, E, E, E, E, E, E,
             "\n".join(wrap(os.environ['field_16'], 38)), E, E, E, E, E, E, E, os.environ['field_17'], E, E],
            # row 6 - Investigation information header
            [os.environ['field_18'], E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E, E],
            # row 7 - EOD manager | name | Vessel | val | Date | val
            [os.environ['field_19'], E, E, E, E, E, value_20, E, E, E, E, E, E, E,
             os.environ['field_19a'], E, value_20a, E, os.environ['field_21'], E, E, value_22, E, E, E],
            # row 8 - Search radius | Object found | Weight | Depth | Size  (+ values)
            [os.environ['field_23'], E, E, E, E, E, os.environ['field_24'], E,
             os.environ['field_25'], E, E, E, E, value_25a,
             os.environ['field_26'], E, value_27, E, "\n".join(wrap(os.environ['field_28'], 10)),
             E, E, value_29, "\n".join(wrap(os.environ['field_30'], 9)), E, value_31],
            # row 9 - Target cleared | val | As found Position | E | easting
            [os.environ['field_32'], E, E, E, E, E, value_33, E, E, E, E, E, E, E,
             "\n".join(wrap(os.environ['field_34'], 30)), E, E, E, E, os.environ['field_35'], value_36, E, E, E, E],
            # row 10 - Clearance depth | val | (position span) | N | northing
            [os.environ['field_37'], E, E, E, E, E, clearance_depth, E, E, E, E, E, E, E,
             E, E, E, E, E, os.environ['field_39'], value_40, E, E, E, E],
            # row 11 - Description | value
            [os.environ['field_41'], E, E, E, E, E, "\n".join(wrap(value_42, 130)), E, E, E, E, E, E, E,
             E, E, E, E, E, E, E, E, E, E, E],
            # row 12 - Comments | value
            [os.environ['field_43'], E, E, E, E, E, "\n".join(wrap(value_43a, 130)), E, E, E, E, E, E, E,
             E, E, E, E, E, E, E, E, E, E, E],
            # row 13 - Images header
            ["\n".join(wrap(os.environ['field_44'], 95)), E, E, E, E, E, E, E, E, E, E, E, E, E,
             E, E, E, E, E, E, E, E, E, E, E],
            # row 14 - target photo 1 | target photo 2
            [image_itp1, E, E, E, E, E, E, E, E, E, E, E, E,
             image_itp2, E, E, E, E, E, E, E, E, E, E, E],
            # row 15 - photo labels
            [os.environ['field_47'], E, E, E, E, E, E, E, E, E, E, E, E,
             os.environ['field_48'], E, E, E, E, E, E, E, E, E, E, E],
            # row 16 - chart image | MAG image
            [image_topo, E, E, E, E, E, E, E, E, E, E, E, E,
             image_tmi, E, E, E, E, E, E, E, E, E, E, E],
            # row 17 - chart labels
            ["\n".join(wrap(os.environ['field_51'], 80)), E, E, E, E, E, E, E, E, E, E, E, E,
             "\n".join(wrap(os.environ['field_52'], 80)), E, E, E, E, E, E, E, E, E, E, E],
            # row 18 - Date/Data | val | QA signature image
            [os.environ['field_53'], E, E, datetime.datetime.now().strftime("%d.%m.%Y"), E, E, E, E, E, E, E, E, E,
             image_qa_signature_edgar_schwab, E, E, E, E, E, E, E, E, E, E, E],
            # row 19 - EOD signature label | EOD signature image | (QA image span)
            [os.environ['field_56'], E, E, E, E, eod_signature, E, E, E, E, E, E, E, E,
             E, E, E, E, E, E, E, E, E, E, E],
            # row 20 - (EOD label span) | EOD name | QA label
            [E, E, E, E, E, value_20, E, E, E, E, E, E, E,
             os.environ['field_55'], E, E, E, E, E, E, E, E, E, E, E],
        ]

        BLUE = '#DAE3F3'
        GREY = '#F2F2F2'

        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Arimo'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),

            # --- row 0: contractor headers + big title ---
            ('SPAN', (0, 0), (7, 0)), ('SPAN', (8, 0), (13, 0)), ('SPAN', (14, 0), (24, 1)),
            ('FONTSIZE', (0, 0), (13, 0), 7),
            ('FONTSIZE', (14, 0), (24, 1), 13), ('FONTNAME', (14, 0), (24, 1), 'Arimo-Bold'),
            ('ALIGN', (14, 0), (24, 1), 'LEFT'), ('VALIGN', (14, 0), (24, 1), 'MIDDLE'),
            ('BACKGROUND', (14, 0), (24, 1), BLUE),

            # --- rows 1-3: logos / address / MTL / target no ---
            ('SPAN', (0, 1), (2, 3)), ('SPAN', (3, 1), (7, 3)), ('SPAN', (8, 1), (13, 3)),
            ('SPAN', (14, 2), (15, 3)), ('SPAN', (16, 2), (24, 3)),
            ('FONTSIZE', (3, 1), (7, 3), 7),
            ('FONTSIZE', (14, 2), (15, 3), 16), ('FONTNAME', (14, 2), (15, 3), 'Arimo-Bold'),
            ('FONTSIZE', (16, 2), (24, 3), 16), ('FONTNAME', (16, 2), (24, 3), 'Arimo-Bold'),
            ('BACKGROUND', (14, 2), (15, 3), BLUE),

            # --- row 4: project / general contractor ---
            ('SPAN', (0, 4), (2, 4)), ('SPAN', (3, 4), (13, 4)), ('SPAN', (14, 4), (21, 4)), ('SPAN', (22, 4), (24, 4)),
            ('ALIGN', (0, 4), (2, 4), 'LEFT'),
            ('ALIGN', (14, 4), (21, 4), 'CENTER'),
            ('FONTSIZE', (3, 4), (13, 4), 6),
            ('BACKGROUND', (0, 4), (2, 4), GREY), ('BACKGROUND', (14, 4), (21, 4), GREY),

            # --- row 5: lokalizacja / project manager ---
            ('SPAN', (0, 5), (2, 5)), ('SPAN', (3, 5), (13, 5)), ('SPAN', (14, 5), (21, 5)), ('SPAN', (22, 5), (24, 5)),
            ('ALIGN', (0, 5), (2, 5), 'LEFT'),
            ('ALIGN', (14, 5), (21, 5), 'CENTER'), ('ALIGN', (22, 5), (24, 5), 'LEFT'),
            ('FONTSIZE', (3, 5), (13, 5), 10),
            ('BACKGROUND', (0, 5), (2, 5), GREY), ('BACKGROUND', (14, 5), (21, 5), GREY),

            # --- row 6: investigation header ---
            ('SPAN', (0, 6), (24, 6)),
            ('FONTSIZE', (0, 6), (24, 6), 9), ('FONTNAME', (0, 6), (24, 6), 'Arimo-Bold'),
            ('BACKGROUND', (0, 6), (24, 6), BLUE),

            # --- row 7: EOD manager / vessel / date ---
            ('SPAN', (0, 7), (5, 7)), ('SPAN', (6, 7), (13, 7)), ('SPAN', (14, 7), (15, 7)),
            ('SPAN', (16, 7), (17, 7)), ('SPAN', (18, 7), (20, 7)), ('SPAN', (21, 7), (24, 7)),
            ('ALIGN', (0, 7), (5, 7), 'LEFT'), ('ALIGN', (14, 7), (15, 7), 'LEFT'), ('ALIGN', (18, 7), (20, 7), 'LEFT'),
            ('BACKGROUND', (0, 7), (5, 7), GREY),
            ('BACKGROUND', (14, 7), (15, 7), GREY), ('BACKGROUND', (18, 7), (20, 7), GREY),

            # --- row 8: search radius / object / weight / depth / size ---
            ('SPAN', (0, 8), (5, 8)), ('SPAN', (6, 8), (7, 8)), ('SPAN', (8, 8), (12, 8)),
            ('SPAN', (14, 8), (15, 8)), ('SPAN', (16, 8), (17, 8)), ('SPAN', (18, 8), (20, 8)),
            ('SPAN', (21, 8), (21, 8)), ('SPAN', (22, 8), (23, 8)),
            ('ALIGN', (0, 8), (5, 8), 'LEFT'), ('ALIGN', (8, 8), (12, 8), 'LEFT'),
            ('ALIGN', (14, 8), (15, 8), 'LEFT'), ('ALIGN', (18, 8), (19, 8), 'LEFT'), ('ALIGN', (22, 8), (23, 8), 'LEFT'),
            ('BACKGROUND', (0, 8), (5, 8), GREY), ('BACKGROUND', (8, 8), (12, 8), GREY),
            ('BACKGROUND', (14, 8), (15, 8), GREY), ('BACKGROUND', (18, 8), (20, 8), GREY),
            ('BACKGROUND', (22, 8), (23, 8), GREY),
            ('LEADING', (22, 8), (23, 8), 7),

            # --- rows 9-10: target cleared / as found position / E / N ---
            ('SPAN', (0, 9), (5, 9)), ('SPAN', (6, 9), (13, 9)),
            ('SPAN', (14, 9), (18, 10)), ('SPAN', (20, 9), (24, 9)),
            ('SPAN', (0, 10), (5, 10)), ('SPAN', (6, 10), (13, 10)), ('SPAN', (20, 10), (24, 10)),
            ('ALIGN', (0, 9), (5, 9), 'LEFT'), ('ALIGN', (0, 10), (5, 10), 'LEFT'),
            ('FONTSIZE', (14, 9), (18, 10), 6), ('VALIGN', (14, 9), (18, 10), 'MIDDLE'),
            ('FONTNAME', (19, 9), (19, 10), 'Arimo-Bold'),
            ('BACKGROUND', (0, 9), (5, 9), GREY), ('BACKGROUND', (0, 10), (5, 10), GREY),
            ('BACKGROUND', (14, 9), (19, 10), BLUE),
            ('LEADING', (0, 9), (5, 9), 9), ('LEADING', (0, 10), (5, 10), 9),

            # --- row 11: description ---
            ('SPAN', (0, 11), (5, 11)), ('SPAN', (6, 11), (24, 11)),
            ('ALIGN', (0, 11), (5, 11), 'LEFT'), ('ALIGN', (6, 11), (24, 11), 'LEFT'),
            ('BACKGROUND', (0, 11), (5, 11), GREY),

            # --- row 12: comments ---
            ('SPAN', (0, 12), (5, 12)), ('SPAN', (6, 12), (24, 12)),
            ('ALIGN', (0, 12), (5, 12), 'LEFT'), ('ALIGN', (6, 12), (24, 12), 'LEFT'),
            ('BACKGROUND', (0, 12), (5, 12), GREY),

            # --- row 13: images header ---
            ('SPAN', (0, 13), (24, 13)),
            ('FONTSIZE', (0, 13), (24, 13), 9), ('FONTNAME', (0, 13), (24, 13), 'Arimo-Bold'),
            ('BACKGROUND', (0, 13), (24, 13), BLUE),

            # --- rows 14-17: image cells + labels ---
            ('SPAN', (0, 14), (12, 14)), ('SPAN', (13, 14), (24, 14)),
            ('SPAN', (0, 15), (12, 15)), ('SPAN', (13, 15), (24, 15)),
            ('SPAN', (0, 16), (12, 16)), ('SPAN', (13, 16), (24, 16)),
            ('SPAN', (0, 17), (12, 17)), ('SPAN', (13, 17), (24, 17)),
            ('FONTNAME', (0, 15), (24, 15), 'Arimo-Bold'),
            ('FONTNAME', (0, 17), (24, 17), 'Arimo-Bold'),

            # --- row 18: bottom date | QA signature image ---
            ('SPAN', (0, 18), (2, 18)), ('SPAN', (3, 18), (12, 18)), ('SPAN', (13, 18), (24, 19)),
            ('ALIGN', (0, 18), (2, 18), 'LEFT'),
            ('BACKGROUND', (0, 18), (2, 18), GREY),

            # --- rows 19-20: signatures ---
            ('SPAN', (0, 19), (4, 20)), ('SPAN', (5, 19), (12, 19)),
            ('SPAN', (5, 20), (12, 20)), ('SPAN', (13, 20), (24, 20)),
            ('ALIGN', (0, 19), (4, 20), 'LEFT'),
            ('FONTNAME', (5, 20), (12, 20), 'Arimo-Bold'),
            ('BACKGROUND', (0, 19), (4, 20), GREY), ('BACKGROUND', (13, 20), (24, 20), GREY),
        ])

        # Column widths (mm) taken proportionally from the Excel template (B..Z)
        col_widths = [7.49, 4.66, 6.5, 4.66, 13.28, 5.93, 13.28, 4.66, 13.28, 13.28, 2.82,
                      4.66, 2.4, 6.22, 13.28, 4.66, 6.92, 10.03, 4.94, 5.51, 4.66, 6.22,
                      5.93, 4.94, 11.73]

        # Row heights (mm) taken from the Excel template (rows 1..21)
        row_heights = [7.64, 4.59, 4.59, 6.35, 11.64, 8.5, 5.03, 7.5, 7.5, 6.5, 7.0,
                       6.35, 6.35, 7.94, 55, 5.03, 55, 4.85, 4.85, 13.76, 5.29]

        t = Table(data,
                  colWidths=[w * mm for w in col_widths],
                  rowHeights=[h * mm for h in row_heights])
        t.setStyle(style)

        elements.append(t)

        doc.build(elements)

        try:
            save_pdf(file_path, 'media/targetrecords/' + str(settings.TARGET_RECORD_PREFIX) + str(
            itp_no_mag) + '(' + value_54 + ').pdf')
        except Exception as e:
            print(f"Error saving PDF '{file_path}':", e)
            return

register_fonts()