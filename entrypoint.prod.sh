#!/bin/sh

echo "Applying migrations..."
python manage.py migrate

python manage.py loaddata fixtures/demo_data.json

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting app..."
exec "$@"