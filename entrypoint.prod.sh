#!/bin/sh

echo "Preparing media directory..."
mkdir -p /usr/src/app/media
chown -R nonroot:nonroot /usr/src/app/media

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting app as nonroot..."
exec su -s /bin/sh nonroot -c "$*"