"""
Django settings for psono project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import socket
import os
import yaml
import json
import hashlib
import nacl.encoding
import nacl.signing
import binascii
import base64
import six
from decimal import Decimal
from urllib.parse import urlparse
from corsheaders.defaults import default_headers
from yubico_client.yubico import DEFAULT_API_URLS as DEFAULT_YUBICO_API_URLS


try:
    # Fall back to psycopg2cffi
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    import psycopg2

HOME = os.path.expanduser('~')


if os.environ.get('PSONO_SERVER_SETTING_BASE64', None):
    config = yaml.safe_load(base64.b64decode(os.environ.get('PSONO_SERVER_SETTING_BASE64', None)))
else:
    with open(os.path.join(HOME, '.psono_server', 'settings.yaml'), 'r') as stream:
        config = yaml.safe_load(stream)




def config_get(key, *args):
    if 'PSONO_' + key in os.environ:
        val = os.environ.get('PSONO_' + key)
        try:
            json_object = json.loads(val)
        except ValueError:
            return val
        return json_object
    if key in config:
        return config.get(key)
    if len(args) > 0:
        return args[0]
    raise Exception("Setting missing", "Couldn't find the setting for %s (maybe you forgot the 'PSONO_' prefix in the environment variable" % (key,))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_get('SECRET_KEY')
PRIVATE_KEY  = config_get('PRIVATE_KEY', '')
PUBLIC_KEY  = config_get('PUBLIC_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(config_get('DEBUG', False)).lower() == 'true'

ALLOWED_HOSTS = config_get('ALLOWED_HOSTS')
ALLOWED_DOMAINS = config_get('ALLOWED_DOMAINS')

ALLOW_REGISTRATION = str(config_get('ALLOW_REGISTRATION', True)).lower() == 'true'
ALLOW_LOST_PASSWORD = str(config_get('ALLOW_LOST_PASSWORD', True)).lower() == 'true'
ENFORCE_MATCHING_USERNAME_AND_EMAIL = str(config_get('ENFORCE_MATCHING_USERNAME_AND_EMAIL', False)).lower() == 'true'
ALLOWED_SECOND_FACTORS = config_get('ALLOWED_SECOND_FACTORS', ['yubikey_otp', 'google_authenticator', 'duo'])
ALLOW_USER_SEARCH_BY_EMAIL = str(config_get('ALLOW_USER_SEARCH_BY_EMAIL', False)).lower() == 'true'
ALLOW_USER_SEARCH_BY_USERNAME_PARTIAL = str(config_get('ALLOW_USER_SEARCH_BY_USERNAME_PARTIAL', False)).lower() == 'true'

DUO_INTEGRATION_KEY = config_get('DUO_INTEGRATION_KEY', '')
DUO_SECRET_KEY = config_get('DUO_SECRET_KEY', '')
DUO_API_HOSTNAME = config_get('DUO_API_HOSTNAME', '')

MULTIFACTOR_ENABLED = str(config_get('MULTIFACTOR_ENABLED', False)).lower() == 'true'

REGISTRATION_EMAIL_FILTER = config_get('REGISTRATION_EMAIL_FILTER', [])

for index in range(len(REGISTRATION_EMAIL_FILTER)):
    REGISTRATION_EMAIL_FILTER[index] = REGISTRATION_EMAIL_FILTER[index].lower().strip()

for index in range(len(ALLOWED_SECOND_FACTORS)):
    ALLOWED_SECOND_FACTORS[index] = ALLOWED_SECOND_FACTORS[index].lower().strip()


HOST_URL = config_get('HOST_URL')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'anymail',
    'corsheaders',
    'rest_framework',
    'restapi',
    'administration',
    'fileserver',
    'credit',
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher'
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'restapi.parsers.DecryptJSONParser',
        # 'rest_framework.parsers.FormParser', # default for Form Parsing
        'rest_framework.parsers.MultiPartParser', # default for UnitTest Parsing
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'restapi.renderers.EncryptJSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1440/day',
        'login': '48/day',
        'link_share_secret': '60/hour',
        'password': '24/day',
        'user': '28800/day',
        'health_check': '61/hour',
        'status_check': '6/minute',
        'ga_verify': '6/minute',
        'duo_verify': '6/minute',
        'yubikey_otp_verify': '6/minute',
        'registration': '20/day',
        'user_delete': '20/day',
        'user_update': '20/day',
        'fileserver_alive': '61/minute',
        'fileserver_upload': '10000/minute',
        'fileserver_download': '10000/minute',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'restapi_query_formatter': {
            '()': 'restapi.log.QueryFormatter',
            'format': '%(time_utc)s logger=%(name)s, %(message)s'
        }
    },
    'filters': {
        'restapi_query_console': {
            '()': 'restapi.log.FilterQueryConsole',
        },
    },
    'handlers': {
        'restapi_query_handler_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'restapi_query_formatter',
            'filters': ['restapi_query_console'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['restapi_query_handler_console'],
        }
    }
}


for key, value in config_get('DEFAULT_THROTTLE_RATES', {}).items():
    REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'][key] = value # type: ignore


ROOT_URLCONF = 'psono.urls'
SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )

CORS_ALLOW_HEADERS = default_headers + (
    'authorization-validator',
    'pragma',
    'if-modified-since',
    'cache-control',
)

TEMPLATES = config_get('TEMPLATES')

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = config_get('DATABASES')

for (db_name, db_values) in six.iteritems(DATABASES):
    for (db_configname, db_value) in six.iteritems(db_values):
        DATABASES[db_name][db_configname] = config_get('DATABASES_' + db_name.upper() + '_' + db_configname.upper(), DATABASES[db_name][db_configname])


EMAIL_FROM = config_get('EMAIL_FROM')
EMAIL_HOST = config_get('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = config_get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config_get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = int(config_get('EMAIL_PORT', 25))
EMAIL_SUBJECT_PREFIX = config_get('EMAIL_SUBJECT_PREFIX', '')
EMAIL_USE_TLS = str(config_get('EMAIL_USE_TLS', False)).lower() == 'true'
EMAIL_USE_SSL = str(config_get('EMAIL_USE_SSL', False)).lower() == 'true'
EMAIL_SSL_CERTFILE = config_get('EMAIL_SSL_CERTFILE', None)
EMAIL_SSL_KEYFILE = config_get('EMAIL_SSL_KEYFILE', None)
EMAIL_TIMEOUT = int(config_get('EMAIL_TIMEOUT', 0)) if config_get('EMAIL_TIMEOUT', 0) else None

YUBIKEY_CLIENT_ID = config_get('YUBIKEY_CLIENT_ID', None)
YUBIKEY_SECRET_KEY = config_get('YUBIKEY_SECRET_KEY', None)
YUBICO_API_URLS = config_get('YUBICO_API_URLS', DEFAULT_YUBICO_API_URLS)

EMAIL_BACKEND = config_get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

ANYMAIL = {
    "MAILGUN_API_URL": config_get('MAILGUN_API_URL', 'https://api.mailgun.net/v3'),  # For EU: https://api.eu.mailgun.net/v3
    "MAILGUN_API_KEY": config_get('MAILGUN_ACCESS_KEY', ''),
    "MAILGUN_SENDER_DOMAIN": config_get('MAILGUN_SERVER_NAME', ''),

    "MAILJET_API_KEY": config_get('MAILJET_API_KEY', ''),
    "MAILJET_SECRET_KEY": config_get('MAILJET_SECRET_KEY', ''),
    "MAILJET_API_URL": config_get('MAILJET_API_URL', 'https://api.mailjet.com/v3'),

    "MANDRILL_API_KEY": config_get('MANDRILL_API_KEY', ''),
    "MANDRILL_API_URL": config_get('MANDRILL_API_URL', 'https://mandrillapp.com/api/1.0'),

    "POSTMARK_SERVER_TOKEN": config_get('POSTMARK_SERVER_TOKEN', ''),
    "POSTMARK_API_URL": config_get('POSTMARK_API_URL', 'https://api.postmarkapp.com/'),

    "SENDGRID_API_KEY": config_get('SENDGRID_API_KEY', ''),
    "SENDGRID_API_URL": config_get('SENDGRID_API_URL', 'https://api.sendgrid.com/v3/'),

    "SENDINBLUE_API_KEY": config_get('SENDINBLUE_API_KEY', ''),
    "SENDINBLUE_API_URL": config_get('SENDINBLUE_API_URL', 'https://api.sendinblue.com/v3/'),

    "SPARKPOST_API_KEY": config_get('SPARKPOST_API_KEY', ''),
    "SPARKPOST_API_URL": config_get('SPARKPOST_API_URL', 'https://api.sparkpost.com/api/v1'),  # For EU: https://api.eu.sparkpost.com/api/v1
}

DEFAULT_FROM_EMAIL = config_get('EMAIL_FROM')

CACHE_ENABLE = str(config_get('CACHE_ENABLE', False)).lower() == 'true'

if str(config_get('CACHE_DB', False)).lower() == 'true':
    CACHES = {
        "default": {
            "BACKEND": 'django.core.cache.backends.db.DatabaseCache',
            "LOCATION": 'restapi_cache',
        }
    }

if str(config_get('CACHE_REDIS', False)).lower() == 'true':
    CACHES = {
       "default": { # type: ignore
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": config_get('CACHE_REDIS_LOCATION', 'redis://localhost:6379/0'),
           "OPTIONS": { # type: ignore
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       }
    }

if not str(config_get('THROTTLING', True)).lower() == 'true':
    CACHES = {
        "default": {
            "BACKEND": 'django.core.cache.backends.dummy.DummyCache',
        }
    }

DISABLE_LAST_PASSWORDS = int(config_get('DISABLE_LAST_PASSWORDS', 0))

MANAGEMENT_ENABLED = str(config_get('MANAGEMENT_ENABLED', False)).lower() == 'true'
FILESERVER_HANDLER_ENABLED = str(config_get('FILESERVER_HANDLER_ENABLED', True)).lower() == 'true'
CREDIT_HANDLER_ENABLED = str(config_get('CREDIT_HANDLER_ENABLED', True)).lower() == 'true'
FILES_ENABLED = str(config_get('FILES_ENABLED', True)).lower() == 'true'

FILE_REPOSITORY_TYPES = [
    'gcp_cloud_storage',
    'aws_s3',
    'do_spaces',
]

FILESERVER_ALIVE_TIMEOUT = int(config_get('FILESERVER_ALIVE_TIMEOUT', 30))
AUTH_KEY_LENGTH_BYTES = int(config_get('AUTH_KEY_LENGTH_BYTES', 64))
USER_PRIVATE_KEY_LENGTH_BYTES = int(config_get('USER_PRIVATE_KEY_LENGTH_BYTES', 80))
USER_PUBLIC_KEY_LENGTH_BYTES = int(config_get('USER_PUBLIC_KEY_LENGTH_BYTES', 32))
USER_SECRET_KEY_LENGTH_BYTES = int(config_get('USER_SECRET_KEY_LENGTH_BYTES', 80))
NONCE_LENGTH_BYTES = int(config_get('NONCE_LENGTH_BYTES', 24))
ACTIVATION_LINK_SECRET = config_get('ACTIVATION_LINK_SECRET')
WEB_CLIENT_URL  = config_get('WEB_CLIENT_URL', '')
DB_SECRET = config_get('DB_SECRET')
EMAIL_SECRET_SALT = config_get('EMAIL_SECRET_SALT')

ACTIVATION_LINK_TIME_VALID = int(config_get('ACTIVATION_LINK_TIME_VALID', 2592000)) # in seconds
DEFAULT_TOKEN_TIME_VALID = int(config_get('DEFAULT_TOKEN_TIME_VALID', 86400)) # 24h in seconds
MAX_WEBCLIENT_TOKEN_TIME_VALID = int(config_get('MAX_WEB_TOKEN_TIME_VALID', 2592000)) # 30d in seconds
MAX_APP_TOKEN_TIME_VALID = int(config_get('MAX_MOBILE_TOKEN_TIME_VALID', 30758400)) # 356d in seconds
RECOVERY_VERIFIER_TIME_VALID = int(config_get('RECOVERY_VERIFIER_TIME_VALID', 600)) # in seconds
REPLAY_PROTECTION_DISABLED = str(config_get('REPLAY_PROTECTION_DISABLED', False)).lower() == 'true' # disables the replay protection
DEVICE_PROTECTION_DISABLED = str(config_get('DEVICE_PROTECTION_DISABLED', False)).lower() == 'true' # disables the device fingerprint protection
REPLAY_PROTECTION_TIME_DFFERENCE = int(config_get('REPLAY_PROTECTION_TIME_DFFERENCE', 20)) # in seconds
DISABLE_CENTRAL_SECURITY_REPORTS = str(config_get('DISABLE_CENTRAL_SECURITY_REPORTS', False)).lower() == 'true' # disables central security reports

# Credit costs
SHARD_CREDIT_BUY_ADDRESS = config_get('SHARD_CREDIT_BUY_ADDRESS', 'https://example.com')
SHARD_CREDIT_DEFAULT_NEW_USER = Decimal(str(config_get('SHARD_CREDIT_DEFAULT_NEW_USER', 0))) # the default credits in Euro for new users
SHARD_CREDIT_COSTS_UPLOAD = Decimal(str(config_get('SHARD_CREDIT_COSTS_UPLOAD', 0))) # costs in Euro for an upload of 1 GB
SHARD_CREDIT_COSTS_DOWNLOAD = Decimal(str(config_get('SHARD_CREDIT_COSTS_DOWNLOAD', 0))) # costs in Euro for a download of 1 GB
SHARD_CREDIT_COSTS_STORAGE = Decimal(str(config_get('SHARD_CREDIT_COSTS_STORAGE', 0))) # costs in Euro for the storage of 1 GB per day

# DEFAULT_FILE_REPOSITORY_ENABLED = str(config_get('DEFAULT_FILE_REPOSITORY_ENABLED', False)).lower() == 'true'
# DEFAULT_FILE_REPOSITORY_UUID = config_get('DEFAULT_FILE_REPOSITORY_ENABLED', '00000000-0000-0000-0000-000000000000') # Don't change this as you might lose access to data
# DEFAULT_FILE_REPOSITORY_TITLE = config_get('DEFAULT_FILE_REPOSITORY_TITLE', 'Default Repository')
# DEFAULT_FILE_REPOSITORY_BUCKET = config_get('DEFAULT_FILE_REPOSITORY_BUCKET', None)
# DEFAULT_FILE_REPOSITORY_TYPE = config_get('DEFAULT_FILE_REPOSITORY_TYPE', 'gcp_cloud_storage')
# DEFAULT_FILE_REPOSITORY_CREDENTIALS = config_get('DEFAULT_FILE_REPOSITORY_CREDENTIALS', None)
# # Read path to config with defaults for environment specific variables
# DEFAULT_FILE_REPOSITORY_CREDENTIAL_PATH = None
#
# if DEFAULT_FILE_REPOSITORY_TYPE == 'gcp_cloud_storage':
#     DEFAULT_FILE_REPOSITORY_CREDENTIAL_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)
#
# DEFAULT_FILE_REPOSITORY_CREDENTIAL_PATH = config_get('DEFAULT_FILE_REPOSITORY_CREDENTIAL_PATH', DEFAULT_FILE_REPOSITORY_CREDENTIAL_PATH)

DATABASE_ROUTERS = ['restapi.database_router.MainRouter']

TIME_SERVER = config_get('TIME_SERVER', 'time.google.com')

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_METHODS = config_get('AUTHENTICATION_METHODS', ['AUTHKEY'])


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'

with open(os.path.join(BASE_DIR, 'VERSION.txt')) as f:
    VERSION = f.readline().rstrip()

HOSTNAME = socket.getfqdn()

with open(os.path.join(BASE_DIR, 'SHA.txt')) as f:
    SHA = f.readline().rstrip()

# Add Sentry logging
SENTRY_DSN = config_get('SENTRY_DSN', '')
if SENTRY_DSN:
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'environment': config_get('SENTRY_ENVIRONMENT', 'development'),
        'release': VERSION,
        'site': PUBLIC_KEY,
    }
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

def generate_signature():

    if WEB_CLIENT_URL:
        web_client = WEB_CLIENT_URL
    else:
        url = urlparse(HOST_URL)
        web_client = url.scheme + '://' + url.netloc

    info = {
        'version': VERSION,
        'api': 1,
        'log_audit': False,
        'public_key': PUBLIC_KEY,
        'authentication_methods': AUTHENTICATION_METHODS,
        'web_client': web_client,
        'management': MANAGEMENT_ENABLED,
        'files': FILES_ENABLED,
        'allowed_second_factors': ALLOWED_SECOND_FACTORS,
        'disable_central_security_reports': DISABLE_CENTRAL_SECURITY_REPORTS,
        'allow_user_search_by_email': ALLOW_USER_SEARCH_BY_EMAIL,
        'allow_user_search_by_username_partial': ALLOW_USER_SEARCH_BY_USERNAME_PARTIAL,
        'system_wide_duo_exists': DUO_SECRET_KEY != '',
        'multifactor_enabled': MULTIFACTOR_ENABLED,
        'type': 'CE',
        'credit_buy_address': SHARD_CREDIT_BUY_ADDRESS,
        'credit_costs_upload': str(SHARD_CREDIT_COSTS_UPLOAD),
        'credit_costs_download': str(SHARD_CREDIT_COSTS_DOWNLOAD),
        'credit_costs_storage': str(SHARD_CREDIT_COSTS_STORAGE),
    }

    info = json.dumps(info)

    signing_box = nacl.signing.SigningKey(PRIVATE_KEY, encoder=nacl.encoding.HexEncoder)
    verify_key = signing_box.verify_key.encode(encoder=nacl.encoding.HexEncoder)
    # The first 128 chars (512 bits or 64 bytes) are the actual signature, the rest the binary encoded info
    signature = binascii.hexlify(signing_box.sign(six.b(info)))[:128]

    return {
        'info': info,
        'signature': signature,
        'verify_key': verify_key,
    }

SIGNATURE = generate_signature()