#!/bin/sh

mkdir -p /usr/src/app/media
chown -R nonroot:nonroot /usr/src/app/media

python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."

python manage.py collectstatic --noinput

echo "Starting app..."

exec "$@"
