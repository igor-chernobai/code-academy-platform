#!/bin/sh

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting app..."
exec "$@"