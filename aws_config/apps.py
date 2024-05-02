from django.apps import AppConfig


class AWSAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aws_config"
    label = "AWSConfig"
