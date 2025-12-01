"""
Django settings for traillend_final_web project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load local .env for development
load_dotenv()

# =========================================================
# BASE DIRECTORY
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECRET KEY / DEBUG
# =========================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "True") == "True"

# =========================================================
# ALLOWED HOSTS
# =========================================================
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "traillend-system-qqo7.onrender.com",
    ".onrender.com",
]


# =========================================================
# INSTALLED APPS
# =========================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_extensions',

    'cloudinary',
    'cloudinary_storage',

    'core.apps.CoreConfig',
]


# =========================================================
# MIDDLEWARE
# =========================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # CORS MUST BE AT THE TOP
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================================
# REST FRAMEWORK + JWT
# =========================================================
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=31),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


CSRF_TRUSTED_ORIGINS = [
    "https://traillend-system-qqo7.onrender.com",
    "https://*.onrender.com",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Fix login issues on Render Free
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"


# Important
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
]


# =========================================================
# URLS / WSGI
# =========================================================
ROOT_URLCONF = 'traillend_final_web.urls'
WSGI_APPLICATION = 'traillend_final_web.wsgi.application'

# =========================================================
# TEMPLATES
# =========================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core' / 'templates',   # <-- THIS IS YOUR FOLDER
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =========================================================
# DATABASE (RENDER)
# =========================================================
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}


# =========================================================
# CLOUDINARY MEDIA STORAGE
# =========================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



# =========================================================
# STATIC FILES
# =========================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / "static" ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================================================
# EMAIL SETTINGS (SENDGRID SMTP)
# =========================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"  # IMPORTANT: literally this text
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = "traillendsystem@gmail.com"




# =========================================================
# INTERNATIONALIZATION
# =========================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True


# =========================================================
# DJANGO DEFAULTS
# =========================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'


# =========================================================
# FIREBASE INITIALIZATION (ENV ONLY)
# =========================================================
from core.firebase import initialize_firebase
initialize_firebase()
