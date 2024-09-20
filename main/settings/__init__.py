import os
import environ

env = environ.Env()
environ.Env.read_env()

if os.environ['DJANGO_ENV'] == 'prod':
    from .prod import *
else:
    from .dev import *
