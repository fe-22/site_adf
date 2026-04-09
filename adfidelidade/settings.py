import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SEGURANÇA ─────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS', ''
).split(',')

# ─── APPS ──────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',

    'core',
    'gestao',
]

# ─── MIDDLEWARE ────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adfidelidade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'adfidelidade.wsgi.application'

# ─── BANCO (SIMPLES - SQLITE) ─────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── INTERNACIONALIZAÇÃO ───────────────────────────────
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ─── STATIC ───────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ─── MEDIA / UPLOAD ───────────────────────────────────
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')

if GS_BUCKET_NAME:
    # GOOGLE CLOUD STORAGE
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

    GS_DEFAULT_ACL = None
    GS_QUERYSTRING_AUTH = False
    GS_FILE_OVERWRITE = False

    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

else:
    # LOCAL (fallback)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# ─── PADRÃO ───────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/painel/login/'
LOGIN_REDIRECT_URL = '/painel/'