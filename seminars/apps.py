from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SeminarsConfig(AppConfig):
    name = "seminars"
    verbose_name = _("Conférences")
