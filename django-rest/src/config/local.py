import os
from .common import Common
import dj_database_url


database_name = os.getenv("DATABASE_NAME", "customer_service")
database_user = os.getenv("DATABASE_USER", "admin")
database_password = os.getenv("DATABASE_PASSWORD", "Admin@2024")
database_port = os.getenv("DATABASE_PORT", "35432")
database_host = os.getenv("DATABASE_HOST", "localhost")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(',')


class Local(Common):
    DEBUG = True

    # Testing
    ALLOWED_HOSTS = ALLOWED_HOSTS
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ("django_nose", "django_seed",)
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
    NOSE_ARGS = [
        # BASE_DIR,
        "-s",
        "--verbosity=2",
        # "--with-coverage",
        # "--with-progressive",
        "--cover-package=src.v1",
        "--debug=unittest",
        "--nologcapture",
        "--exe"
    ]

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
