from django.apps import AppConfig


class ElevAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elev_app'

    def ready(self):
        '''
        Running the another thread containing infinite loop
        '''
        from .utils import RunThread
        RunThread().start()