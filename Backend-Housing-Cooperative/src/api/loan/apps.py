from django.apps import AppConfig


class LoanConfig(AppConfig):
    name = 'api.loan'
    
    def ready(self):
        from . import signals
