"""
WSGI config for location_progiciel project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys
from pathlib import Path

# Ajouter le dossier apps au PYTHONPATH (identique à settings)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'apps'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_wsgi_application()