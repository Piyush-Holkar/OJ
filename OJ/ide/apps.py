from django.apps import AppConfig
import os
from django.conf import settings


class IdeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ide"

    def ready(self):
        runtime_dirs = [
            settings.CODES_DIR,
            settings.INPUTS_DIR,
            settings.OUTPUTS_DIR,
        ]

        for directory in runtime_dirs:
            os.makedirs(directory, exist_ok=True)
