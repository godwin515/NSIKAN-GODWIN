from django.apps import AppConfig



class SchoolwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schoolweb'

    def ready(self):
        import schoolweb.signals   # noqa