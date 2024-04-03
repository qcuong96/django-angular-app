import os
from .common import Common

database_name = os.getenv("DATABASE_NAME", "dummy")
database_user = os.getenv("DATABASE_USER", "dummy")
database_password = os.getenv("DATABASE_PASSWORD", "dummy")
database_port = os.getenv("DATABASE_PORT", "dummy")
database_host = os.getenv("DATABASE_HOST", "dummy")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(',')

secrect_key = os.getenv(
    "DJANGO_SECRET_KEY", "dummy"
)


class Staging(Common):
    DEBUG = True
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = secrect_key
    ALLOWED_HOSTS = ALLOWED_HOSTS
    INSTALLED_APPS += ("gunicorn", )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': database_name,
            'USER': database_user,
            'PASSWORD': database_password,
            'HOST': database_host,
            'PORT': database_port,
        }
    }
