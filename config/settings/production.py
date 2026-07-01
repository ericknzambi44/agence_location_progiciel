# config/settings/production.py
# Fichier de configuration pour l'environnement de production (Render).
# Il hérite de base.py et surcharge les paramètres sensibles.

from .base import *
from decouple import config
import dj_database_url
import sys

# ============================================================
# 1. MODE DEBUG – Toujours désactivé en production
# ============================================================
DEBUG = False

# ============================================================
# 2. HÔTES AUTORISÉS – Doit inclure l'URL de Render
# ============================================================
# Lecture depuis .env, séparés par des virgules.
# Exemple : ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# ============================================================
# 3. BASE DE DONNÉES – Priorité à DATABASE_URL (fournie par Render)
# ============================================================
# Render injecte automatiquement DATABASE_URL si vous avez lié un service PostgreSQL.
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Utiliser la chaîne de connexion complète fournie par Render.
    # dj_database_url parse automatiquement l'URL et gère SSL.
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,        # Garder la connexion ouverte 10 minutes
            ssl_require=True         # Forcer SSL pour PostgreSQL
        )
    }
else:
    # Fallback (uniquement pour les tests locaux) – jamais utilisé sur Render.
    # Fournir des valeurs par défaut pour éviter l'erreur "not found".
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='location_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'CONN_MAX_AGE': 60,
        }
    }

# ============================================================
# 4. FICHIERS STATIQUES ET MÉDIAS
# ============================================================
# Les fichiers statiques sont collectés dans ce dossier (utilisé par Gunicorn).
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# ============================================================
# 5. SÉCURITÉ HTTPS – Obligatoire sur Render
# ============================================================
# Redirige toutes les requêtes HTTP vers HTTPS.
SECURE_SSL_REDIRECT = True
# Les cookies de session et CSRF ne sont envoyés qu'en HTTPS.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# HSTS : Force le navigateur à utiliser HTTPS pendant 1 an.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ============================================================
# 6. CONFIGURATION EMAIL (Gmail avec port 465 SSL)
# ============================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')                  # smtp.gmail.com
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)  # 465
EMAIL_HOST_USER = config('EMAIL_HOST_USER')        # nokigence@gmail.com
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # mot de passe d'application
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)  # True si port 465
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# ============================================================
# 7. REST FRAMEWORK – Désactiver l'interface browsable en prod
# ============================================================
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',   # Uniquement du JSON
]
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.IsAuthenticated',
]

# ============================================================
# 8. LOGGING – Journalisation vers la console (utile pour Render)
# ============================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# ============================================================
# 9. CORRECTION CORS – Assurez-vous que ces variables sont définies
#    dans les variables d'environnement de Render.
#    Elles sont déjà lues dans base.py via CORS_ALLOWED_ORIGINS et
#    CORS_ALLOW_CREDENTIALS.
# ============================================================
# Les paramètres CORS sont déjà configurés dans base.py, mais
# vous pouvez les surcharger ici si nécessaire.
# Exemple de valeurs (si vous voulez les forcer) :
# CORS_ALLOWED_ORIGINS = ['https://votre-frontend.onrender.com', ...]
# CORS_ALLOW_CREDENTIALS = True
# ATTENTION : Ne pas écraser les valeurs lues dans base.py sans raison.