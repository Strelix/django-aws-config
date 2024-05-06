from pathlib import Path
from aws_config.settings_handler import AWSSharedSettingsDict, AWSConfig, AWSHandler

AWSHandler.set_shared({
        "region_name": "eu-west-2",
        "custom_cdn_domain": "https://cdn.example.com",
        "path_prefix": "my_site/"
    })

# AWSHandler.

AWSHandler.set_configs(
    configs=[
        AWSConfig(
            option="media_private",
            access_key_id="AWS_ACCESS_KEY_ID",
            access_key="AWS_SECRET_ACCESS_KEY",
            region_name="eu-west-2",
            custom_cdn_domain="private_media.example.com",
            bucket_name="static_files_bucket",
        ),
        AWSConfig(
            option="static",
            access_key_id="AWS_ACCESS_KEY_ID",
            access_key="AWS_SECRET_ACCESS_KEY",
            region_name="eu-west-2",
            custom_cdn_domain="static.example.com",
            bucket_name="static_files_bucket",
        )
    ]
)

STORAGES = AWSHandler._get_storages_dict()
print(STORAGES)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+6nhhao3&&)290_+&9$-=p3*-@_1KJ7bzz%0csn2j*3&4-d8%Z'

default_app_config = 'example.example.apps.ExampleConfig'

ADMIN_ENABLED = False

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "aws_config",
    "example"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'example.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
