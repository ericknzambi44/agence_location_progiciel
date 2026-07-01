#!/bin/bash

# Appliquer les migrations (avec gestion d'erreur)
python manage.py migrate --noinput || echo "Migrations failed, continuing..."

# Collecter les fichiers statiques
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."

# Exécuter la commande passée en argument (gunicorn)
exec "$@"