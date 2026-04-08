#!/bin/sh
set -e

echo "Rodando migrate..."
python manage.py migrate --noinput

echo "Criando superusuario se nao existir..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$DJANGO_SUPERUSER_USERNAME'
password = '$DJANGO_SUPERUSER_PASSWORD'
if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='', password=password)
    print('Superusuario criado:', username)
else:
    print('Superusuario ja existe ou variaveis nao configuradas.')
"

echo "Iniciando gunicorn..."
exec gunicorn adfidelidade.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120
