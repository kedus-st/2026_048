from django.conf import settings

def media_url(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'GEODATA_URL': settings.GEODATA_URL,
        'PROJECT_NAME': settings.PROJECT_NAME,
        'EPSG': settings.EPSG,
    }
    return context