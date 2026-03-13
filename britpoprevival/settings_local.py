from .settings import *

SECRET_KEY = "local-dev-secret-key"
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "xPqhg63sder01",
        "HOST": "localhost",
        "PORT": "5432",
    }
}