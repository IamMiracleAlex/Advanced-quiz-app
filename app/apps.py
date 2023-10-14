from django.apps import AppConfig as MyAppConfig

from pinax.referrals.apps import AppConfig as PinaxConfig



class ReferralConfig(PinaxConfig):
    verbose_name = 'Referrals'


class AppConfig(MyAppConfig):
    name = 'app'
    verbose_name = "Applications"


    def ready(self):
        import app.signals #noqa
        

