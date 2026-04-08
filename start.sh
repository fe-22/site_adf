#!/bin/sh
set -e

echo "Rodando migrate..."
python manage.py migrate --noinput

echo "Iniciando gunicorn..."
exec gunicorn adfidelidade.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120
