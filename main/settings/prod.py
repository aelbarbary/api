from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'nozolan_marriage',
#         'OPTIONS': {
#                 'read_default_file': '/etc/mysql/my.cnf',
#                 'charset': 'utf8mb4'
#         },
#     }
# }

# SMTP_USER_NAME=env('SMTP_USER_NAME')
# SMTP_PASSWORD=env('SMTP_PASSWORD')


AWS_STORAGE_BUCKET_NAME = 'marriage-media'
AWS_S3_REGION_NAME = 'us-east-1' 
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        # Adding the watchtower handler here causes all loggers in the project that
        # have propagate=True (the default) to send messages to watchtower. If you
        # wish to send only from specific loggers instead, remove "watchtower" here
        # and configure individual loggers below.
        'handlers': ['watchtower'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'watchtower': {
            'class': 'watchtower.CloudWatchLogHandler',
            'boto3_client': boto3_logs_client,
            'log_group_name': 'nozolan-marriage',
            # Decrease the verbosity level here to send only those logs to watchtower,
            # but still see more verbose logs in the console. See the watchtower
            # documentation for other parameters that can be set here.
            'level': 'ERROR'
        }
    },
    'loggers': {
        # In the debug server (`manage.py runserver`), several Django system loggers cause
        # deadlocks when using threading in the logging handler, and are not supported by
        # watchtower. This limitation does not apply when running on production WSGI servers
        # (gunicorn, uwsgi, etc.), so we recommend that you set `propagate=True` below in your
        # production-specific Django settings file to receive Django system logs in CloudWatch.
        'django': {
            'level': 'ERROR',
            'handlers': [],
            'propagate': False
        }
        # Add any other logger-specific configuration here.
    }
}
