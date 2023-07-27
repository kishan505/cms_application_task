from django.apps import AppConfig


class CmsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CMS_app'

    def ready(self):
        import CMS_app.signals