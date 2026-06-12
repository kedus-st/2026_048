from django.apps import AppConfig

class ClearanceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clearance_app'
    verbose_name = 'Clearance'

class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from . import dash_app
