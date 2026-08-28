"""
Production settings for elearn project.
"""

import os
import dj_database_url
from .base import *

DEBUG = False

ADMINS = [
    ('Admin', 'admin@example.com'),
]

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-prod-key-change-in-env')

# Allowed hosts
ALLOWED_HOSTS = ['*']

raw_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
if raw_hosts:
    ALLOWED_HOSTS = [
        host.strip().replace('*.', '.')
        for host in raw_hosts.split(',')
        if host.strip()
    ]
    if '*' in raw_hosts:
        ALLOWED_HOSTS.append('*')

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Trust Render SSL Proxy Header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.railway.app',
    'https://*.up.railway.app',
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override database from DATABASE_URL environment variable if set
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'], conn_max_age=500)

# Production Channel Layer using environment REDIS_URL or local fallback
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# Security headers and SSL/TLS for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# SSL/TLS & HTTPS settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
