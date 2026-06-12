from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management'

class DPRStatAppConfig(AppConfig):
    name = 'dpr_dash_app'

    def ready(self):
        from . import dpr_dash_app