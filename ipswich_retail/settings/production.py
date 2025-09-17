"""
Production settings for Ipswich Retail
"""
import os
import dj_database_url
from pathlib import Path
from .base import *

# Build paths inside the project - override from base
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security Settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Allow Render.com domain
ALLOWED_HOSTS = [
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Get the Render hostname if available
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Database Configuration - Use PostgreSQL in production
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"[STARTUP] DATABASE_URL configured: {bool(DATABASE_URL)}")
print(f"[STARTUP] Database URL value: {DATABASE_URL[:50] if DATABASE_URL else 'Not set'}...")

if DATABASE_URL:
    print("[STARTUP] Using PostgreSQL database")
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    print("[STARTUP] WARNING: Using SQLite fallback - DATABASE_URL not set!")
    # Fallback to SQLite for initial deployment
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Headers
# Disable SSL redirect for Render (handles SSL termination at proxy level)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False  # Disabled for Render
CSRF_COOKIE_SECURE = False  # Disabled for Render
CSRF_TRUSTED_ORIGINS = ['https://ipswich-retail.onrender.com']
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email Configuration (optional)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}