from django.conf import settings

import os


def get_setting(name: str, default=None):
    if name in os.environ:
        return os.environ[name]
    return getattr(settings, name, default)
