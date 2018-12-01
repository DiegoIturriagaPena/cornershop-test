"""Configuration for Development."""

from .base import *

import os

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Periodicity
PERIODICITY = 1

# SLACK
SLACK_TOKEN = 'xoxb-293351272678-wSKCUxU7kpliAictKiSCYJJS'
SLACK_CHANNEL = '#general'  # almuerzo
