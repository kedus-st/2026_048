from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Image, SimpleDocTemplate
from textwrap import wrap

import os, datetime, django

from PIL import Image as PILImage
import requests
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clearance.settings')
django.setup()

from clearance import settings

from backend.blob_actions import list_blobs, overwrite_tr, delete_img, overwrite_duplicate, upload_xyz


from clearance_app.models import MtlItem

'''
Return overwrite_tr and save_pdf functions to create_tr in models.py after successful tests 
Uncomment query line at start of create_tr
Revert def create_tr(itp_no_mag) to create_tr(self, itp_no_mag)
Revery file_path
'''

def create_tr(itp_no_mag):
        print("Starting recreation")
        #query = self.__class__.objects.get(itp_no_mag=itp_no_mag)
        query = itp_no_mag

        #overwrite_tr(str(itp_no_mag))

        if(None in [query.clear, query.found, query.eod] or '' in [query.clear, query.found, query.eod]):
            return
        elif ('y' not in query.qa_clear or 'y' not in query.clear):
            return
        value_08 = itp_no_mag
        value_20 = query.eod
        value_22 = query.cl_date
        value_22a = query.cl_time
        value_25a = query.found
        if 'y' in value_25a:
            value_25a = 'Y'
        if 'n' in value_25a:
            value_25a = 'N'
        value_27 = query.cl_weight
        value_29 = query.cl_depth_bg
        value_823 = query.cl_length
        value_923 = query.cl_width

        # Avoid 'None', make empty instead
        value_31 = (str(query.cl_length) + '/\n' + str(query.cl_width)).replace('None/\nNone', '')

        value_33 = query.clear
        if 'y' in value_33:
            value_33 = 'Y'
        if 'n' in value_33:
            value_33 = 'N'

        value_34 = query.salvaged
        if 'y' in value_34:
            value_34 = 'Y'
        elif 'n' in value_34:
            value_34 = 'N'
        else:
            value_34 = ''

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

        value_41a_string = query.description_detail
        value_41a = ''
        if query.description_detail is not None:
            if len(query.description_detail) > 122:
                # value_43a = value_43a_string[:121] + '\n' + value_43a_string[121:]
                value_41a = value_41a_string.replace('\\n', '\n')
            else:
                value_41a = value_41a_string
        else:
            value_41a = ''

        value_54 = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        value_54a = datetime.datetime.now().strftime("%d.%m.%Y")

        value_713 = itp_no_mag.vessel
        value_1124 = itp_no_mag.water_depth_geoid
        
        
        value_1224 = query.uxo
        try:
            if 'x' in value_1224:
                value_1224 = 'Y'
            else:
                value_1224 = 'N'
        except:
            value_1224 = 'N'


        mtlimages = list_blobs('media/mtlimages/')
        magimages = list_blobs('media/magimages/')
        afimages = list_blobs('media/rovimages/af/pngs')
        alimages = list_blobs('media/rovimages/al/pngs')
        aftracks = list_blobs('media/rovtracks/af/pngs')
        altracks = list_blobs('media/rovtracks/al/pngs')
        sssimages = list_blobs('media/sssimages/')
        mbesimages = list_blobs('media/mbesimages/')
        topoimages250 = list_blobs('media/topoimages250/')
        topoimages5000 = list_blobs('media/topoimages5000/')
        # image_itp = Image(os.path.join(settings.ITP_IMAGES_ROOT, 'MTL-1401_pic_1.JPG'))

        if(settings.PROJECT_NAME+'/media/mtlimages/'+str(itp_no_mag) + '_pic_1.jpg' in mtlimages):      
        #if(any(str(itp_no_mag) + '_pic_1.jpg') in imgs for imgs in mtlimages):            
        #try:
            image_itp = Image(
                os.path.join(settings.ITP_IMAGES_ROOT, str(itp_no_mag) + '_pic_1.jpg'))
            image_itp.drawHeight = 53 * mm
            image_itp.drawWidth = 74 * mm
        else:
            image_itp = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_itp.drawHeight = 53 * mm
            image_itp.drawWidth = 74 * mm

        # if os.path.isfile(os.path.join(settings.MAG_IMAGES_ROOT, str(itp_no_mag) + '_TFEM_IMAGE.png')):
        #     image_tfem = Image(os.path.join(settings.MAG_IMAGES_ROOT, str(itp_no_mag) + '_TFEM_IMAGE.png'))
        #     image_tfem.drawWidth = 90 * mm
        #     image_tfem.drawHeight = 45 * mm
        # else:
        #     image_tfem = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
        #     image_tfem.drawHeight = 53 * mm
        #     image_tfem.drawWidth = 74 * mm

        if(settings.PROJECT_NAME+'/media/magimages/'+str(itp_no_mag) + '_TMI_IMAGE.png' in magimages):
        #if(any(str(itp_no_mag) + '_TMI_IMAGE.png') in imgs for imgs in magimages):
        #try:
            image_tmi = Image(os.path.join(settings.MAG_IMAGES_ROOT, str(itp_no_mag) + '_TMI_IMAGE.png'))
            image_tmi.drawWidth = 102 * mm
            image_tmi.drawHeight = 54 * mm
        else:
            image_tmi = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_tmi.drawHeight = 53 * mm
            image_tmi.drawWidth = 74 * mm

        # try:
        #     image_topo = Image(os.path.join(settings.TOPO_IMAGES_ROOT, str(itp_no_mag) + '_TOPO_IMAGE.png'))
        #     image_topo.drawWidth = 90 * mm
        #     image_topo.drawHeight = 45 * mm
        # except OSError as e:
        #     image_topo = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
        #     image_topo.drawHeight = 53 * mm
        #     image_topo.drawWidth = 74 * mm

        if(settings.PROJECT_NAME+'/media/rovimages/af/pngs/'+str(itp_no_mag) + '-af.png' in afimages):
        #if(any(str(itp_no_mag) + '_TOPO_IMAGE.png') in imgs for imgs in topoimages):
        #try:
            image_af = Image(os.path.join(settings.ROV_AF_IMAGES_ROOT, 'pngs', str(itp_no_mag) + '-af.png'))
            image_af.drawWidth = 102 * mm
            image_af.drawHeight = 54 * mm
        else:
            image_af = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_af.drawHeight = 53 * mm
            image_af.drawWidth = 74 * mm
        
        if(settings.PROJECT_NAME+'/media/rovimages/al/pngs/'+str(itp_no_mag) + '-al.png' in alimages):
        #try:
            image_al = Image(os.path.join(settings.ROV_AL_IMAGES_ROOT, 'pngs', str(itp_no_mag) + '-al.png'))
            image_al.drawHeight = 54 * mm
            image_al.drawWidth = 102 * mm
        else:
            image_al = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_al.drawHeight = 53 * mm
            image_al.drawWidth = 74 * mm
        
        if(settings.PROJECT_NAME+'/media/rovtracks/af/pngs/'+str(itp_no_mag) + '-af-tracks.png' in aftracks):
        #if(any(str(itp_no_mag) + '_TOPO_IMAGE.png') in imgs for imgs in topoimages):
        #try:
            image_af_tracks = Image(os.path.join(settings.ROV_AF_TRACKS_ROOT, 'pngs', str(itp_no_mag) + '-af-tracks.png'))
            image_af_tracks.drawWidth = 53 * mm
            image_af_tracks.drawHeight = 53 * mm
        else:
            image_af_tracks = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_af_tracks.drawHeight = 53 * mm
            image_af_tracks.drawWidth = 74 * mm
        
        if(settings.PROJECT_NAME+'/media/rovtracks/al/pngs/'+str(itp_no_mag) + '-al-tracks.png' in altracks):
        #if(any(str(itp_no_mag) + '_TOPO_IMAGE.png') in imgs for imgs in topoimages):
        #try:
            image_al_tracks = Image(os.path.join(settings.ROV_AL_TRACKS_ROOT, 'pngs', str(itp_no_mag) + '-al-tracks.png'))
            image_al_tracks.drawWidth = 53 * mm
            image_al_tracks.drawHeight = 53 * mm
        else:
            image_al_tracks = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_al_tracks.drawHeight = 53 * mm
            image_al_tracks.drawWidth = 74 * mm

        if(settings.PROJECT_NAME+'/media/sssimages/'+str(itp_no_mag) + '_SSS_IMAGE.png' in sssimages):
        #if(any(str(itp_no_mag) + '_TMI_IMAGE.png') in imgs for imgs in magimages):
        #try:
            image_sss = Image(os.path.join(settings.SSS_IMAGES_ROOT, str(itp_no_mag) + '_SSS_IMAGE.png'))
            image_sss.drawWidth = 53 * mm
            image_sss.drawHeight = 53 * mm
        else:
            image_sss = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_sss.drawHeight = 53 * mm
            image_sss.drawWidth = 74 * mm

        if(settings.PROJECT_NAME+'/media/mbesimages/'+str(itp_no_mag) + '_MBES_IMAGE.png' in mbesimages):
        #if(any(str(itp_no_mag) + '_TMI_IMAGE.png') in imgs for imgs in magimages):
        #try:
            image_mbes = Image(os.path.join(settings.MBES_IMAGES_ROOT, str(itp_no_mag) + '_MBES_IMAGE.png'))
            image_mbes.drawWidth = 53 * mm
            image_mbes.drawHeight = 53 * mm
        else:
            image_mbes = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_mbes.drawHeight = 53 * mm
            image_mbes.drawWidth = 74 * mm

        try:
            if 'y' in query.clear:
                hatch = PILImage.open(os.path.join(settings.STATIC_ROOT, 'img/green_x.png'))
            elif 'w' in query.clear:
                hatch = PILImage.open(os.path.join(settings.STATIC_ROOT, 'img/yellow_x.png'))
            else:
                hatch = PILImage.open(os.path.join(settings.STATIC_ROOT, 'img/red_x.png'))
        except:
            hatch = PILImage.open(os.path.join(settings.STATIC_ROOT, 'img/red_x.png'))

        if(settings.PROJECT_NAME+'/media/topoimages250/'+str(itp_no_mag) + '_TOPO_IMAGE_250.png' in topoimages250):
        #if(any(str(itp_no_mag) + '_TMI_IMAGE.png') in imgs for imgs in magimages):
        #try:
            response = requests.get(os.path.join(settings.TOPO_IMAGES_250_ROOT, str(itp_no_mag) + '_TOPO_IMAGE_250.png'))
            topo_image = PILImage.open(BytesIO(response.content))
            overlay = PILImage.alpha_composite(topo_image.convert('RGBA'), hatch.convert('RGBA'))
            overlay.save("tmp/overlaid_image.png")                          
            image_topo250 = Image('tmp/overlaid_image.png')
            image_topo250.drawWidth = 53 * mm
            image_topo250.drawHeight = 53 * mm
        else:
            image_topo250 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_topo250.drawHeight = 53 * mm
            image_topo250.drawWidth = 74 * mm

        if(settings.PROJECT_NAME+'/media/topoimages5000/'+str(itp_no_mag) + '_TOPO_IMAGE_5000.png' in topoimages5000):
        #if(any(str(itp_no_mag) + '_TMI_IMAGE.png') in imgs for imgs in magimages):
        #try:
            image_topo5000 = Image(os.path.join(settings.TOPO_IMAGES_5000_ROOT, str(itp_no_mag) + '_TOPO_IMAGE_5000.png'))
            image_topo5000.drawWidth = 53 * mm
            image_topo5000.drawHeight = 53 * mm
        else:
            image_topo5000 = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            image_topo5000.drawHeight = 53 * mm
            image_topo5000.drawWidth = 74 * mm

        image_clinet_logo = Image(os.path.join(settings.IMAGES_ROOT, 'client_logo.png'))
        image_clinet_logo.drawWidth = 18 * mm
        image_clinet_logo.drawHeight = 16 * mm

        image_seaterra_logo = Image(os.path.join(settings.IMAGES_ROOT, 'seaterra_logo.png'))
        image_seaterra_logo.drawWidth = 16 * mm
        image_seaterra_logo.drawHeight = 10 * mm

        # EOD SIGNATURES

        if value_20.startswith('Tjerk Reichel'):
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
        elif value_20.startswith('Dominik Nowak'):
            eod_signature = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/dominik_nowak_signature.png'))
            eod_signature.drawHeight = 12 * mm
            eod_signature.drawWidth = 24 * mm
        else:
            eod_signature = Image(os.path.join(settings.STATIC_ROOT, 'img/no_image.png'))
            eod_signature.drawHeight = 8 * mm
            eod_signature.drawWidth = 28 * mm

        image_qa_signature_edgar_schwab = Image(os.path.join(settings.IMAGES_ROOT, 'signatures/edgar_schwab_signature.png'))
        image_qa_signature_edgar_schwab.drawHeight = 15 * mm
        image_qa_signature_edgar_schwab.drawWidth = 40 * mm

        file_path = 'tmp/' + str(settings.TARGET_RECORD_PREFIX) + str(
            itp_no_mag) + '(' + value_54 + ').pdf'
        
        file_path = 'tmp/test.pdf'

        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=10 * mm, leftMargin=10 * mm, topMargin=1 * mm,
                                bottomMargin=0 * mm)
        doc.pagesize = portrait(A4)
        elements = []

        '''
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
        '''

        data = [

            #HEADER START

            [os.environ['field_01'], '1', '2', '3', '4', '5', os.environ['field_02'], '7', '8', '9', '10', '11', '12', 
             os.environ['field_03'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
             
            [image_clinet_logo, '1', os.environ['field_05'],'3', '4', '5', image_seaterra_logo, '7', os.environ['field_63'], '9', '10','11', '12', 
             '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
             os.environ['field_07'], '14', '15', value_08, '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 
            '14', '15', '16', '17', '18','19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_09'], '1','2', os.environ['field_10'], '4', '5', '6', '7', '8', '9', '10', '11', '12', 
             os.environ['field_11'], '14', '15', '16', '17', '18', '19', '20', '21', os.environ['field_12'], '23', '24', '25' ],

            [os.environ['field_13'], '1','2', '', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
             os.environ['field_16'], '14', '15', '16', '17', '18', '19', '20', '21', os.environ['field_17'], '23', '24', '25' ],
            
            #HEADER END

            #INVESTIGATION INFORMATION START

            [os.environ['field_18'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_19'], '1', '2', '3', '4', '5', '6', '7', value_20, '9', '10', '11', '12',
             os.environ['field_64'], '14', '15', value_713, '17', '18', os.environ['field_21a'], '20', '21', str(value_22)+"\n"+str(value_22a)[:-3], '23', '24'],
            
            [os.environ['field_23'], '1', '2', '3', '4', '5', os.environ['field_24'], os.environ['field_25'], '8', '9', '10', '11', 
             value_25a, os.environ['field_26'], '14', '15', value_27, os.environ['field_28'], '18', '19', value_29, os.environ['field_30'], '22', '23', value_823, '25'],
            
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', value_923, '25'],

            [os.environ['field_32'], '1', '2', '3', '4', '5', value_33, os.environ['field_65'], '8', '9', '10', '11', 
             value_34, os.environ['field_34'], '14', '15', '16', 'E', value_36, '19', os.environ['field_66'], '21', '22', '23', value_1124, '25'],

            [os.environ['field_67'], '1', '2', '3', '4', '5', os.environ['field_68'], '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', 'N', value_40, '19', 'UXO (Y/N)', '21', '22', '23', value_1224, '25'],

            [os.environ['field_41'], '1', '2', '3', '4', '5', value_41a, '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            
            [os.environ['field_43'], '1', '2', '3', '4', '5', value_43a, '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            #INVESTIGATION INFORMATION END

            #IMAGES START

            [os.environ['field_44a'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [image_itp, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            image_tmi, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_47'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            os.environ['field_48'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [image_af, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            image_al, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_51'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            os.environ['field_52'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            #IMAGES END

            #PAGE ROW START
            [os.environ['field_73'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '1', '25'],
            #PAGE ROW END

            #SECOND PAGE

            #HEADER START

            [os.environ['field_01'], '1', '2', '3', '4', '5', os.environ['field_02'], '7', '8', '9', '10', '11', '12', 
             os.environ['field_03'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
             
            [image_clinet_logo, '1', os.environ['field_05'], '3', '4', '5', image_seaterra_logo, '7', os.environ['field_63'], '9', '10','11', '12', 
             '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],


            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
             os.environ['field_07'], '14', '15', value_08, '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', 
            '14', '15', '16', '17', '18','19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_09'], '1','2', os.environ['field_10'], '4', '5', '6', '7', '8', '9', '10', '11', '12', 
             os.environ['field_11'], '14', '15', '16', '17', '18', '19', '20', '21', os.environ['field_12'], '23', '24', '25' ],

            [os.environ['field_13'], '1','2', value_63, '4', '5', '6', '7', '8', '9', '10', '11', '12', 
             os.environ['field_16'], '14', '15', '16', '17', '18', '19', '20', '21', os.environ['field_17'], '23', '24', '25' ],
            
            #HEADER END

            #IMAGES START

            [os.environ['field_44'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [image_af_tracks, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            image_al_tracks, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_74'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            os.environ['field_75'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [image_sss, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            image_mbes, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_76'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            os.environ['field_77'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [image_topo250, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            image_topo5000, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],

            [os.environ['field_78'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            os.environ['field_79'], '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25'],
            
            #IMAGES END

            #FOOTER START
            [os.environ['field_69'], '1', '2', '3', '4', os.environ['field_19'], '6', '7', '8', '9', '10', '11', os.environ['field_58'],
            '13', '14', '15', '16', '17', '18', os.environ['field_58'], '20', '21', '22', '23', '24', '25'],
            [os.environ['field_70'], '1', '2', '3', '4', os.environ['field_71']+"\n"+value_20, '6', '7', '8', '9', '10', '11', os.environ['field_72'],
            '13', '14', '15', '16', '17', '18', os.environ['field_62'], '20', '21', '22', '23', '24', '25'],
            [os.environ['field_21'], '1', '2', '3', '4', value_54a, '6', '7', '8', '9', '10', '11', value_54a,
            '13', '14', '15', '16', '17', '18', '', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_56'], '1', '2', '3', '4', eod_signature, '6', '7', '8', '9', '10', '11', image_qa_signature_edgar_schwab,
            '13', '14', '15', '16', '17', '18', '', '20', '21', '22', '23', '24', '25'],
            [os.environ['field_43'], '1', '2', '3', '4', '', '6', '7', '8', '9', '10', '11', '',
            '13', '14', '15', '16', '17', '18', '', '20', '21', '22', '23', '24', '25'],
            #FOOTER END

            #PAGE ROW START
            [os.environ['field_73'], '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '2', '25'],
            #PAGE ROW END

        ]

        # table = Table(data, colWidths=7*mm, rowHeights=5*mm)

        #('BACKGROUND', (13, 0), (25, 2), '#DAE3F3'),


        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),

            #HEADER START
            ('BACKGROUND', (13, 0), (25, 3), '#DAE3F3'),
            ('FONTSIZE', (13, 0), (25, 3), 16),
            ('VALIGN', (13, 2), (25, 2), 'TOP'),
            ('FONTNAME', (13, 0), (25, 3), 'Helvetica-Bold'),

            ('SPAN', (0, 0), (5, 0)), ('SPAN', (6, 0), (12, 0)), ('SPAN', (13, 0), (25, 1)),

            ('SPAN', (0, 1), (1, 3)), ('SPAN', (2, 1), (5, 3)), ('SPAN', (6, 1), (7, 3)), ('SPAN', (8, 1), (12, 3)),
            ('SPAN', (13, 2), (15, 3)), ('SPAN', (16, 2), (25, 3)),
            #('FONTSIZE', (3, 1), (5, 3), 7),
            #('FONTSIZE', (9, 1), (12, 3), 7),

            ('SPAN', (0, 4), (2, 4)), ('SPAN', (3, 4), (12, 4)), ('SPAN', (13, 4), (21, 4)), ('SPAN', (22, 4), (25, 4)),
        
            ('SPAN', (0, 5), (2, 5)), ('SPAN', (3, 5), (12, 5)), ('SPAN', (13, 5), (21, 5)), ('SPAN', (22, 5), (25, 5)),

            #HEADER END

            #INVESTIGATION INFORMATION START

            ('BACKGROUND', (0, 6), (25, 6), '#DAE3F3'),
            ('FONTSIZE', (0, 6), (25, 6), 13),
            ('FONTNAME', (0, 6), (25, 6), 'Helvetica-Bold'),
            ('VALIGN', (0, 6), (25, 6), 'TOP'),

            ('SPAN', (0, 6), (25, 6)),

            ('SPAN', (0, 7), (7, 7)), ('SPAN', (8, 7), (12, 7)),
            ('SPAN', (13, 7), (15, 7)), ('SPAN', (16, 7), (18, 7)),('SPAN', (19, 7), (21, 7)), ('SPAN', (22, 7), (25, 7)),

            ('SPAN', (0, 8), (5, 9)), ('SPAN', (6, 8), (6, 9)), ('SPAN', (7, 8), (11, 9)), ('SPAN', (12, 8), (12, 9)), ('SPAN', (13, 8), (15, 9)),
            ('SPAN', (16, 8), (16, 9)), ('SPAN', (17, 8), (19, 9)), ('SPAN', (20, 8), (20, 9)), ('SPAN', (21, 8), (23, 9)), ('SPAN', (24, 8), (25, 8)), ('SPAN', (24, 9), (25, 9)),

            ('SPAN', (0, 10), (5, 10)), ('SPAN', (6, 10), (6, 10)), ('SPAN', (7, 10), (11, 10)), ('SPAN', (12, 10), (12, 10)),
            ('SPAN', (13, 10), (16, 11)), ('SPAN', (17, 10), (17, 10)), ('SPAN', (17, 10), (17, 10)), ('SPAN', (18, 10), (19, 10)), ('SPAN', (20, 10), (23, 10)), ('SPAN', (24, 10), (25, 10)),

            ('SPAN', (0, 11), (5, 11)), ('SPAN', (6, 11), (12, 11)),
            ('SPAN', (17, 11), (17, 11)), ('SPAN', (17, 11), (17, 11)), ('SPAN', (18, 11), (19, 11)), ('SPAN', (20, 11), (23, 11)), ('SPAN', (24, 11), (25, 11),),

            ('SPAN', (0, 12), (5, 12)), ('SPAN', (6, 12), (25, 12)),

            ('SPAN', (0, 13), (5, 13)), ('SPAN', (6, 13), (25, 13)),

            #INVESTIGATION INFORMATION END

            #IMAGES START

            ('BACKGROUND', (0, 14), (25, 14), '#DAE3F3'),
            ('FONTSIZE', (0, 14), (25, 14), 11),
            ('FONTNAME', (0, 14), (25, 14), 'Helvetica-Bold'),

            ('SPAN', (0, 14), (25, 14)),
            
            ('SPAN', (0, 15), (12, 15)), ('SPAN', (13, 15), (25, 15)),

            ('SPAN', (0, 16), (12, 16)), ('SPAN', (13, 16), (25, 16)),
            
            ('SPAN', (0, 17), (12, 17)), ('SPAN', (13, 17), (25, 17)),

            ('SPAN', (0, 18), (12, 18)), ('SPAN', (13, 18), (25, 18)),

            #IMAGES END

            ('SPAN', (0, 19), (23, 19)), ('SPAN', (24, 19), (25, 19)),
            ('ALIGN', (0, 19), (23, 19), 'RIGHT'),

            #SECOND PAGE
            
            #HEADER START
            ('BACKGROUND', (13, 20), (25, 23), '#DAE3F3'),
            ('FONTSIZE', (13, 20), (25, 23), 16),
            ('FONTNAME', (13, 20), (25, 23), 'Helvetica-Bold'),

            ('SPAN', (0, 20), (5, 20)), ('SPAN', (6, 20), (12, 20)), ('SPAN', (13, 20), (25, 21)),
            #('FONTSIZE', (0, 20), (12, 20), 7.5),

            ('SPAN', (0, 21), (1, 23)), ('SPAN', (2, 21), (5, 23)), ('SPAN', (6, 21), (7, 23)), ('SPAN', (8, 21), (12, 23)),
            ('SPAN', (13, 22), (15, 23)), ('SPAN', (16, 22), (25, 23)),

            ('SPAN', (0, 24), (2, 24)), ('SPAN', (3, 24), (12, 24)), ('SPAN', (13, 24), (21, 24)), ('SPAN', (22, 24), (25, 24)),

            ('SPAN', (0, 25), (2, 25)), ('SPAN', (3, 25), (12, 25)), ('SPAN', (13, 25), (21, 25)), ('SPAN', (22, 25), (25, 25)),

            #HEADER END

            #IMAGES START

            ('BACKGROUND', (0, 26), (25, 26), '#DAE3F3'),
            ('FONTSIZE', (0, 26), (25, 26), 9),
            ('FONTNAME', (0, 26), (25, 26), 'Helvetica-Bold'),

            ('SPAN', (0, 26), (25, 26)),

            ('SPAN', (0, 27), (12, 27)), ('SPAN', (13, 27), (25, 27)),

            ('SPAN', (0, 28), (12, 28)), ('SPAN', (13, 28), (25, 28)),

            ('SPAN', (0, 29), (12, 29)), ('SPAN', (13, 29), (25, 29)),

            ('SPAN', (0, 30), (12, 30)), ('SPAN', (13, 30), (25, 30)),

            ('SPAN', (0, 31), (12, 31)), ('SPAN', (13, 31), (25, 31)),

            ('SPAN', (0, 32), (12, 32)), ('SPAN', (13, 32), (25, 32)),

            #IMAGES END

            #FOOTER START
            ('SPAN', (0, 33), (4, 33)), ('SPAN', (5, 33), (11, 33)), ('SPAN', (12, 33), (18, 33)), ('SPAN', (19, 33), (25, 33)),

            ('SPAN', (0, 34), (4, 34)), ('SPAN', (5, 34), (11, 34)), ('SPAN', (12, 34), (18, 34)), ('SPAN', (19, 34), (25, 34)),

            ('SPAN', (0, 35), (4, 35)), ('SPAN', (5, 35), (11, 35)), ('SPAN', (12, 35), (18, 35)), ('SPAN', (19, 35), (25, 35)),

            ('SPAN', (0, 36), (4, 36)), ('SPAN', (5, 36), (11, 36)), ('SPAN', (12, 36), (18, 36)), ('SPAN', (19, 36), (25, 36)),

            ('SPAN', (0, 37), (4, 37)), ('SPAN', (5, 37), (11, 37)), ('SPAN', (12, 37), (18, 37)), ('SPAN', (19, 37), (25, 37)),

            ('SPAN', (0, 38), (23, 38)), ('SPAN', (24, 38), (25, 38)),
            ('ALIGN', (0, 38), (23, 38), 'RIGHT'),
            #FOOTER END

            #PAGE ROW START
            ('SPAN', (0, 38), (23, 38)), ('SPAN', (24, 38), (25, 38)),
            ('ALIGN', (0, 38), (23, 38), 'RIGHT'),
            #PAGE ROW END

        ])
        

        t = Table(data, colWidths=7.8 * mm,
                  rowHeights=[
                      #HEADER START
                      9 * mm,
                      9 * mm,
                      4.5 * mm,
                      4.5 * mm,
                      8 * mm,
                      8 * mm,
                      #HEADER END

                      #INVESTIGATION INFORMATION START
                      7.5 * mm,
                      9 * mm,
                      5.5 * mm,
                      5.5 * mm,
                      11.0 * mm,
                      13 * mm,
                      21.0 * mm,
                      26.0 * mm,
                      #INVESTIGATION INFORMATION END

                      #IMAGES START
                      12 * mm,
                      55 * mm,
                      9 * mm,
                      55 * mm,
                      9 * mm,
                      #IMAGES END

                      #PAGE ROW START
                      3.5 * mm,
                      #PAGE ROW END

                      #SECOND PAGE

                      #HEADER START
                      9 * mm,
                      9 * mm,
                      4.5 * mm,
                      4.5 * mm,
                      8 * mm,
                      8 * mm,
                      #HEADER END

                      #IMAGES START
                      5.5 * mm,
                      55 * mm,
                      12.5 * mm,
                      55 * mm,
                      8 * mm,
                      55 * mm,
                      8 * mm,
                      #IMAGES END

                      #FOOTER START
                      8.0 * mm,
                      8.0 * mm,
                      4.5 * mm,
                      14.0 * mm,
                      11.0 * mm,
                      #FOOTER END

                      #PAGE ROW START
                      3.5 * mm,
                      #PAGE ROW END

                  ])
        t.setStyle(style)

        elements.append(t)

        doc.build(elements)

        #save_pdf(file_path, 'media/targetrecords/' + str(settings.TARGET_RECORD_PREFIX) + str(
        #    itp_no_mag) + '(' + value_54 + ').pdf')

itp_no_mag = MtlItem.objects.filter(itp_no_mag__exact='ITP-1582')[0]
create_tr(itp_no_mag)