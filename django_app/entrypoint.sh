#!/bin/sh

set -e

echo "Waiting for PostgreSQL database..."
if [ "$POSTGRES_HOST" ]; then
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.5
    done
    echo "PostgreSQL database ready!"
fi

echo "Applying database migrations..."
python manage.py makemigrations accounts patients diagnosis reports dashboard history notifications system_settings --noinput
python manage.py migrate --noinput

echo "Seeding default data..."
python manage.py seed_data || true

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting Django Web Server..."
exec "$@"
