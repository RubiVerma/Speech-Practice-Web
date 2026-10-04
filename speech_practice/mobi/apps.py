from django.apps import AppConfig


class MobiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobi'

    def ready(self):
        import mobi.signals
