from .settings import *

SECRET_KEY = "your-production-secret-key"
DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "britpoprevival_db",
        "USER": "britpoprevival_db_user",
        "PASSWORD": "MyPassword",
        "HOST": "dpg-d6q1f3sr85hc73clfkug-a",
        "PORT": "5432",
    }
}