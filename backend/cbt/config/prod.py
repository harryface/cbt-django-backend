from .base import *  # noqa: F403,F401


EMAIL_BACKEND = str(os.getenv("EMAIL_BACKEND"))
EMAIL_HOST = str(os.getenv("EMAIL_HOST"))
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_HOST_USER =  str(os.getenv("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD =  str(os.getenv("EMAIL_HOST_PASSWORD"))
EMAIL_USE_TLS =  bool(os.getenv("EMAIL_USE_TLS"))
DEFAULT_FROM_EMAIL =  str(os.getenv("DEFAULT_FROM_EMAIL"))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("POSTGRES_DB", "database1"),
        'USER': os.getenv("POSTGRES_USER", "database1_role"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "database1_password"),
        'HOST': os.getenv("POSTGRES_DB", "database1"),
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = list(os.getenv('ALLOWED_HOSTS'))

# importing logger settings
try:
    from .logger_settings import LOGGING 
except Exception as e:
    pass

SECURE_BROWSER_XSS_FILTER = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 20842880
FILE_UPLOAD_MAX_MEMORY_SIZE = 20842880


# If we are using redis cache
# https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://django@localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "EdvjGKaz1tHyDEy0eLyUsoPjNFCDBX1i4qi/kjw5EET///m4Dt0BvTdmCJgR17xb1QJqUSJcW0ipYl+1"
        }
    }
}

# do not forget to run pip install django-redis==5.0.0 redis==3.5.3
