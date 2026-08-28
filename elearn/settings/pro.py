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

# Allowed hosts parsed from environment or defaults
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.railway.app',
    'https://*.up.railway.app',
]

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

# Security headers for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
