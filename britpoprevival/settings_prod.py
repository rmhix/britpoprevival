from .settings import *

SECRET_KEY = "your-production-secret-key"
DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "britpoprevival_db",
        "USER": "britpoprevival_db_user",
        "PASSWORD": "PDVeh98cgr6dX98y26ZN81vHEBTITPp4",
        "HOST": "dpg-d6q1f3sr85hc73clfkug-a.ohio-postgres.render.com",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "require",
    }
}