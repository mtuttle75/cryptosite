from django.apps import AppConfig


class PortfoliosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolios'

    def ready(self):
        from assetUpdater import updater
        updater.start()