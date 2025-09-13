from django.apps import AppConfig

class TodAppBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_app_backend'

    def ready(self):
        from .tokens import start_cleanTokenExpiry
        start_cleanTokenExpiry()
