#!/bin/sh

python manage.py migrate

python manage.py loaddata fixtures/demo_data.json

exec "$@"
