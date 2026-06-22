import sys
from pathlib import Path
from decouple import config

# Chemin absolu vers la racine du projet (là où se trouve manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ajoute le dossier 'apps' au PYTHONPATH pour que Django trouve les modules
sys.path.insert(0, str(BASE_DIR / 'apps'))

# --- Lecture des variables sensibles depuis .env ---
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-votre-cle-ici-pour-dev')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# --- Configuration CORS (Cross-Origin Resource Sharing) ---
# Origines autorisées à accéder à l'API (ex: frontend React)
# Exemple dans .env : CORS_ALLOWED_ORIGINS=http://localhost:1420,http://127.0.0.1:1420
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
# Autoriser l'envoi de cookies / credentials dans les requêtes cross-origin
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=False, cast=bool)

# IMPORTANT : Ne jamais mettre CORS_ALLOW_ALL_ORIGINS=True en production.
# Pour le développement uniquement, vous pouvez décommenter la ligne suivante :
# CORS_ALLOW_ALL_ORIGINS = True if DEBUG else False

# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',  # Gestion des en-têtes CORS

    # Modules métier
    'stock',
    'maintenance',
    'rh',
    'administration',
    'authentication',
    'location',
]

# --- Middleware (ordre crucial) ---
MIDDLEWARE = [
    # CorsMiddleware doit être placé aussi haut que possible,
    # avant les middlewares qui peuvent générer des réponses (ex: CommonMiddleware)
    'corsheaders.middleware.CorsMiddleware',

    # Gère les en-têtes de sécurité (HSTS, XSS, etc.)
    'django.middleware.security.SecurityMiddleware',

    # Gère les sessions utilisateur (nécessaire pour l'admin et l'authentification)
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Middleware commun (gestion des URL, etc.)
    'django.middleware.common.CommonMiddleware',

    # Protection CSRF (Cross-Site Request Forgery)
    'django.middleware.csrf.CsrfViewMiddleware',

    # Associe l'utilisateur aux requêtes (nécessaire après SessionMiddleware)
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Gère les messages flash (utilisés dans l'admin)
    'django.contrib.messages.middleware.MessageMiddleware',

    # Protection contre le clickjacking (X-Frame-Options)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# --- Base de données (SQLite par défaut, surchargeable) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Validation des mots de passe ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalisation ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# --- Fichiers statiques ---
STATIC_URL = 'static/'

# --- Clé primaire par défaut ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuration Django REST Framework ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Pour l'admin
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Interface browsable (utile en dev)
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}