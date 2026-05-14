#!/bin/sh

# Wait for database if needed (optional since it's an external server)
# but good for stability
echo "Waiting for database..."
# You can add a netcat check here if you want to ensure DB is up

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-log -
