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

def create_tr(mtl_item):
        print("Starting recreation")
        #query = self.__class__.objects.get(itp_no_mag=itp_no_mag)
        query = mtl_item

        itp_no_mag = query.itp_no_mag

        overwrite_tr(str(itp_no_mag))

        #if(None in [query.clear, query.found, query.eod] or '' in [query.clear, query.found, query.eod]):
        #    return
        #elif ('y' not in query.qa_clear or 'y' not in query.clear):
        #    return
        if query.clear is None:
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
        # image_itp = Image(os.path.join(settings.ITP_IMAGES_ROOT, 'MTL-1401_pic_1.JPG'))

        images = MtlItemImage.objects.filter(mtl_item__itp_no_mag=itp_no_mag)
        if images.exists():
            if images[0].mtl_item_image.name:
                image_itp1 = Image(get_secure_blob_url(images[0].mtl_item_image.name))
                image_itp1.drawHeight = 53 * mm
                image_itp1.drawWidth = 74 * mm
            else:
                image_itp1 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
                image_itp1.drawHeight = 53 * mm
                image_itp1.drawWidth = 74 * mm
            if images.count() > 1:
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

        if False:#(settings.PROJECT_NAME+'/media/magimages/'+str(itp_no_mag) + '_TMI_IMAGE.png' in magimages):      
            image_tmi = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/magimages/'+str(itp_no_mag) + '_TMI_IMAGE.png'))
            image_tmi.drawHeight = 53 * mm
            image_tmi.drawWidth = 53 * mm
        else:
            image_tmi = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_tmi.drawHeight = 53 * mm
            image_tmi.drawWidth = 74 * mm

        if False:#(settings.PROJECT_NAME+'/media/sssimages/'+str(itp_no_mag) + '_SSS_IMAGE.png' in sssimages):
            image_sss = Image(get_secure_blob_url(settings.PROJECT_NAME+'/media/sssimages/'+str(itp_no_mag) + '_SSS_IMAGE.png'))
            image_sss.drawWidth = 53 * mm
            image_sss.drawHeight = 53 * mm
        else:
            image_sss = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_sss.drawHeight = 53 * mm
            image_sss.drawWidth = 74 * mm

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
        image_clinet_logo.drawWidth = 13 * mm
        image_clinet_logo.drawHeight = 12 * mm

        image_seaterra_logo = Image(os.path.join(settings.IMAGES_ROOT, 'seaterra_logo.png'))
        image_seaterra_logo.drawWidth = 22 * mm
        image_seaterra_logo.drawHeight = 15 * mm

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

        data = [
            [os.environ['field_01'], '1', '2', '3', '4', '5', '6', '7', os.environ['field_02'], '9', '10', '11', '12',
             os.environ['field_03'], '14',
             '15',
             '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            ["\n".join(wrap(os.environ['field_05'], 32)), '1', '2', '3', '4', '5', '6', '7', image_seaterra_logo, '9', '10',
             '11',
             '12', '13',
             '14', '15', '', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '', '14', '15', '16', '17', '18',
             '19',
             '20', '21', '22', '23', '24', '25'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', os.environ['field_07'], '14', '15',
             value_08,
             '17',
             '18', '19', '20', '21', '22', '23', '24', '25'],
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
             '19',
             '20', '21', '22', '23', '24', '25'],
            [os.environ['field_09'], '1', '2', '3', "\n".join(wrap(os.environ['field_10'], 40)), '5', '6', '7', '8', '9', '10', '11', '12',
             os.environ['field_11'], '14',
             '15',
             '16',  "\n".join(wrap(os.environ['field_12'], 42)), '18', '19', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_13'], '1', '2', '3', os.environ['field_14'], '5', '6', '7', '8', '9',
             '10', '11', '12',
             os.environ['field_16'], '14',
             '15', '16', "\n".join(wrap(os.environ['field_17'], 37)), '18', '19', '20', '21', '22', '23', '24', '25'],
            # Investigation Information
            [os.environ['field_18'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
             '16',
             '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_19'], '1', '2', '3', '4', '5', value_20, '7', '8', '9', '10', '11', '12', '13', '14',
             '15',
             '16',
             "\n".join(wrap(os.environ['field_21'],25)), '18', '19', '20', value_22, '22', '23', '24', '25'],
            [os.environ['field_23'], '1', '2', '3', '4', '5', os.environ['field_24'], '7', os.environ['field_25'], '9',
             '10', '11', value_25a,
             os.environ['field_26'],
             '14', value_27, '16', "\n".join(wrap(os.environ['field_28'], 20)), '18', '19', value_29, '21', os.environ['field_30'], '23',
             '24', value_31],
            [os.environ['field_32'], '1', '2', '3', '4', '5', value_33, '7', '8', '9', '10', '11', '12',
             "\n".join(wrap(os.environ['field_34'], 20)), '14',
             '15', '16',
             os.environ['field_35'], '18', value_36, '20', '21', '22', '23', '24', '25'],
            [os.environ['field_37'], '1', '2', '3', '4', '5', '2.5m', '7', '8', '9', '10', '11', '12',
             '', '14', '15',
             '16',
             os.environ['field_39'], '18', value_40, '20', '21', '22', '23', '24', '25'],
            [os.environ['field_41'], '1', '2', '3', '4', '5', "\n".join(wrap(value_42, 120)), '7', '8', '9', '10', '11', '12', '13', '14',
             '15',
             '16', '17',
             '18', '19', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_43'], '1', '2', '3', '4', '5', "\n".join(wrap(value_43a, 120)), '7', '8', '9', '10', '11', '12', '13', '14',
             '15',
             '16', '17',
             '18', '19', '20', '21', '22', '23', '24', '25'],
            ["\n".join(wrap(os.environ['field_44'], 80)), '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
             '16',
             '17', '18',
             '19', '20', '21', '22', '23', '24', '25'],
            [image_itp1, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', image_tmi, '14', '15', '16',
             '17',
             '18', '19', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_47'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
             os.environ['field_48'], '14', '15',
             '16',
             '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            [image_sss, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', image_mbes, '14', '15',
             '16', '17',
             '18', '19', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_51'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
             os.environ['field_52'], '14', '15',
             '16',
             '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            #SIGNATURES
            [os.environ['field_53'], '1', '2', '3', '4', '5', '6', '7', value_54, '9', '10', '11', '12', os.environ['field_55'], '14', '15',
             '16',
             '17',
             image_qa_signature_edgar_schwab, '19', '20', '21', '22', '23', '24', '25'],
            ['', '1', '2', '3', '4', '5', '6', '7', '', '9', '10', '11',
             '12',
             os.environ['field_58'], '14', '15', '16', '17', os.environ['field_60'], '19', '20', '21', '22', '23', '24',
             '25'],

        ]

        # table = Table(data, colWidths=7*mm, rowHeights=5*mm)

        style = TableStyle([

            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('SPAN', (0, 0), (7, 0)), ('SPAN', (8, 0), (12, 0)), ('SPAN', (13, 0), (25, 2)),
            ('FONTSIZE', (0, 0), (7, 0), 7), ('FONTSIZE', (8, 0), (12, 0), 6), ('FONTSIZE', (13, 0), (25, 2), 16),
            ('FONTNAME', (13, 0), (25, 2), 'Helvetica-Bold'),
            ('BACKGROUND', (13, 0), (25, 2), '#DAE3F3'),

            ('SPAN', (0, 1), (7, 4)), ('SPAN', (8, 1), (12, 4)),
            ('SPAN', (13, 3), (15, 4)),
            ('SPAN', (16, 3), (25, 4)),
            ('FONTSIZE', (0, 1), (7, 4), 9),
            ('FONTSIZE', (3, 1), (7, 4), 10), ('FONTSIZE', (13, 3), (15, 4), 16), ('FONTSIZE', (16, 3), (25, 4), 16),
            ('FONTNAME', (13, 3), (15, 4), 'Helvetica-Bold'), ('FONTNAME', (16, 3), (25, 4), 'Helvetica-Bold'),
            ('BACKGROUND', (13, 3), (25, 4), '#DAE3F3'),
            ('VALIGN', (13, 3), (25, 4), 'TOP'),

            ('SPAN', (0, 5), (3, 5)), ('SPAN', (4, 5), (12, 5)), ('SPAN', (13, 5), (16, 5)),
            ('FONTSIZE', (4, 5), (12, 5), 8),
            ('LEADING', (4, 5), (12, 5), 8),
            ('SPAN', (17, 5), (25, 5)),
            ('FONTSIZE', (17, 5), (25, 5), 9),
            ('LEADING', (17, 5), (25, 5), 9),
            ('ALIGN', (0, 5), (25, 5), 'LEFT'),
            ('BACKGROUND', (0, 5), (3, 5), '#F2F2F2'),

            ('SPAN', (0, 6), (3, 6)), ('SPAN', (4, 6), (12, 6)),
            ('SPAN', (13, 6), (16, 6)),
            ('SPAN', (17, 6), (25, 6)),
            ('ALIGN', (0, 6), (25, 6), 'LEFT'),
            ('ALIGN', (6, 6), (12, 6), 'CENTER'),
            ('BACKGROUND', (0, 6), (3, 6), '#F2F2F2'),

            # INvestigation Information
            ('SPAN', (0, 7), (25, 7)),
            ('ALIGN', (0, 7), (25, 7), 'LEFT'),
            ('FONTSIZE', (0, 7), (25, 7), 10),
            ('FONTNAME', (0, 7), (25, 7), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 7), (25, 7), '#DAE3F3'),

            ('SPAN', (0, 8), (5, 8)), ('SPAN', (6, 8), (16, 8)), ('SPAN', (17, 8), (20, 8)),
            ('SPAN', (21, 8), (25, 8)),
            ('FONTSIZE', (0, 8), (25, 8), 7),
            ('ALIGN', (0, 8), (5, 8), 'LEFT'),
            ('BACKGROUND', (0, 8), (5, 8), '#F2F2F2'),
            ('BACKGROUND', (17, 8), (20, 8), '#F2F2F2'),

            # fields 23 - 31
            ('SPAN', (0, 9), (5, 9)),
            ('SPAN', (6, 9), (7, 9)),
            ('SPAN', (8, 9), (11, 9)),
            ('SPAN', (12, 9), (12, 9)),
            ('SPAN', (13, 9), (14, 9)),
            ('SPAN', (15, 9), (16, 9)),
            ('SPAN', (17, 9), (19, 9)),
            ('SPAN', (20, 9), (21, 9)),
            ('SPAN', (22, 9), (24, 9)),
            ('SPAN', (25, 9), (25, 9)),
            ('FONTSIZE', (0, 9), (25, 9), 7),
            ('ALIGN', (0, 9), (5, 9), 'LEFT'),
            ('BACKGROUND', (0, 9), (5, 9), '#F2F2F2'),
            ('BACKGROUND', (8, 9), (11, 9), '#F2F2F2'),
            ('BACKGROUND', (13, 9), (14, 9), '#F2F2F2'),
            ('BACKGROUND', (17, 9), (19, 9), '#F2F2F2'),
            ('BACKGROUND', (22, 9), (24, 9), '#F2F2F2'),
            # end fields 23 - 31

            ('SPAN', (0, 10), (5, 10)), ('SPAN', (6, 10), (12, 10)), ('SPAN', (13, 10), (16, 11)),
            ('SPAN', (17, 10), (18, 10)), ('SPAN', (19, 10), (25, 10)),
            ('FONTSIZE', (0, 10), (25, 10), 7),
            ('ALIGN', (0, 10), (5, 10), 'LEFT'),
            ('BACKGROUND', (0, 10), (5, 10), '#F2F2F2'),
            ('BACKGROUND', (13, 10), (18, 11), '#F2F2F2'),

            ('SPAN', (0, 11), (5, 11)), ('SPAN', (6, 11), (12, 11)), ('SPAN', (13, 11), (16, 11)),
            ('SPAN', (17, 11), (18, 11)), ('SPAN', (19, 11), (25, 11)),
            ('FONTSIZE', (0, 11), (25, 11), 7),
            ('ALIGN', (0, 11), (5, 11), 'LEFT'),
            ('BACKGROUND', (0, 11), (5, 11), '#F2F2F2'),

            ('SPAN', (0, 12), (5, 12)), ('SPAN', (6, 12), (25, 12)),
            ('FONTSIZE', (0, 12), (25, 12), 7),
            ('ALIGN', (0, 12), (5, 12), 'LEFT'),
            ('BACKGROUND', (0, 12), (5, 12), '#F2F2F2'),

            # TR Comment
            ('SPAN', (0, 13), (5, 13)), ('SPAN', (6, 13), (25, 13)),
            ('FONTSIZE', (0, 13), (25, 13), 7),
            ('ALIGN', (0, 13), (5, 13), 'LEFT'),
            ('ALIGN', (6, 13), (25, 13), 'LEFT'),
            ('BACKGROUND', (0, 13), (5, 13), '#F2F2F2'),

            # Images
            ('SPAN', (0, 14), (25, 14)),
            ('ALIGN', (0, 14), (25, 14), 'CENTER'),
            ('FONTSIZE', (0, 14), (25, 14), 10),
            ('FONTNAME', (0, 14), (25, 14), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 14), (25, 14), '#DAE3F3'),

            ('SPAN', (0, 15), (12, 15)), ('SPAN', (13, 15), (25, 15)),
            ('SPAN', (0, 16), (12, 16)), ('SPAN', (13, 16), (25, 16)),
            ('SPAN', (0, 17), (12, 17)), ('SPAN', (13, 17), (25, 17)),
            ('SPAN', (0, 18), (12, 18)), ('SPAN', (13, 18), (25, 18)),
            ('FONTSIZE', (0, 18), (25, 18), 10),
            # End Images
            ('SPAN', (0, 19), (7, 19)), ('SPAN', (8, 19), (12, 19)), ('SPAN', (13, 19), (17, 19)), ('SPAN', (18, 19), (25, 19)),
            ('ALIGN', (0, 19), (3, 19), 'LEFT'),

            ('SPAN', (0, 20), (7, 20)), ('SPAN', (8, 20), (12, 20)), ('SPAN', (13, 20), (17, 20)), ('SPAN', (18, 20), (25, 20)),
            ('ALIGN', (0, 20), (3, 20), 'LEFT'),

        ])

        t = Table(data, colWidths=7 * mm,
                  rowHeights=[
                      4.5 * mm,
                      4.5 * mm,
                      4.5 * mm,
                      4.5 * mm,
                      4.5 * mm,
                      14 * mm,
                      9 * mm,
                      8 * mm,
                      8 * mm,
                      8 * mm,
                      8 * mm,
                      8 * mm,
                      8 * mm,
                      20 * mm,
                      8 * mm,
                      55 * mm,
                      6 * mm,
                      55 * mm,
                      5 * mm,
                      11 * mm,
                      11 * mm,
                      # 6 * mm,
                      # 6 * mm,
                      # 15 * mm,
                      # 6 * mm
                  ])
        t.setStyle(style)

        elements.append(t)

        doc.build(elements)

        #try:
        #    save_pdf(file_path, 'media/targetrecords/' + str(settings.TARGET_RECORD_PREFIX) + str(
        #    itp_no_mag) + '(' + value_54 + ').pdf')
        #except Exception as e:
        #    print(f"Error saving PDF '{file_path}':", e)
        #    return
