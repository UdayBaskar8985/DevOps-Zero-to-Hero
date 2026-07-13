from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'

    def ready(self):
        from .signals import create_default_categories
        post_migrate.connect(create_default_categories, sender=self)
