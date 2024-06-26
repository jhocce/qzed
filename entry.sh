#!/bin/sh

echo "PostgreSQL started"
python manage.py migrate
exec "$@"