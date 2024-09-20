from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '../db.sqlite3',
    }
}

EMAIL_BACKEND = "mailer.backend.DbBackend"
EMAIL_USE_TLS = True
BACKEND_DOMAIN = 'http://localhost:8000'

# LOGGING = {

# }
