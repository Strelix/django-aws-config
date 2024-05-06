from typing import Optional

from django.conf import settings

import os


def get_setting(name: str, default=None, *, fail_if_missing: bool = False) -> Optional[str | bool | int]:
    if name in os.environ:
        return os.environ[name]

    value = getattr(settings, name, default)
    if fail_if_missing and value is None:
        raise ValueError(f"Missing setting: {name}")
    return value
