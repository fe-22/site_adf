"""
Django settings for adfidelidade project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SEGURANÇA ────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-@ma=t%!pi59@rtj#awy#v16p$&hah1b)ohisd+8w$0c^k)z$$y')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_ENV.split(',') if h.strip()] if ALLOWED_HOSTS_ENV else ['*']

# CSRF: aceita domínios de ALLOWED_HOSTS (https) + variável explícita opcional
_csrf_extra = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
_csrf_from_hosts = [
    f'https://{h.strip()}'
    for h in ALLOWED_HOSTS_ENV.split(',')
    if h.strip() and not h.strip() in ('localhost', '127.0.0.1', '*')
]
_csrf_from_env = [o.strip() for o in _csrf_extra.split(',') if o.strip()]
CSRF_TRUSTED_ORIGINS = _csrf_from_hosts + _csrf_from_env or ['http://localhost:8000']


# Application definition

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
        'DIRS': [],
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


# ─── BANCO DE DADOS ───────────────────────────────────────────────────────────
# Em produção use DATABASE_URL ou variáveis individuais.
# Localmente usa SQLite por padrão.
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL:
    import urllib.parse as _up
    _r = _up.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _r.path.lstrip('/'),
            'USER': _r.username,
            'PASSWORD': _r.password,
            'HOST': _r.hostname,
            'PORT': _r.port or 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# ─── ARQUIVOS ESTÁTICOS ───────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ─── ARQUIVOS DE MÍDIA (uploads) ──────────────────────────────────────────────
# Em produção defina GS_BUCKET_NAME para usar o Google Cloud Storage.
# As credenciais são lidas do arquivo apontado por GOOGLE_APPLICATION_CREDENTIALS
# ou automaticamente quando rodando no Google Cloud Run / App Engine.
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME', '')

if GS_BUCKET_NAME:
    # ── Google Cloud Storage ──────────────────────────────────────────────────
    GS_DEFAULT_ACL = None          # bucket com "Acesso uniforme" (recomendado)
    GS_QUERYSTRING_AUTH = False    # URLs públicas sem assinatura
    GS_FILE_OVERWRITE = False      # evita sobrescrever arquivos com mesmo nome
    MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
            'OPTIONS': {
                'bucket_name': GS_BUCKET_NAME,
            },
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }
else:
    # ── Armazenamento local (desenvolvimento) ─────────────────────────────────
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/painel/login/'
LOGIN_REDIRECT_URL = '/painel/'
