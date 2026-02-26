from django.apps import AppConfig


class WalletConfig(AppConfig):
    name = 'api.wallet'
    
    def ready(self):
        import api.wallet.signals 
