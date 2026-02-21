#!/bin/sh

python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."

python manage.py collectstatic --noinput

echo "Starting app..."

exec "$@"
