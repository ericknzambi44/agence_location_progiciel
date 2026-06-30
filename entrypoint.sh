#!/bin/bash

# Appliquer les migrations
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Exécuter la commande passée en argument (gunicorn)
exec "$@"