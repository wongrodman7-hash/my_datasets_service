#!/usr/bin/env bash

echo "Start backend server"

# Wait for backend directory to be available
until cd /app/backend/server
do
    echo "Waiting for server volume..."
    sleep 2
done

# Apply database migrations
until ./manage.py migrate
do
    echo "Waiting for database to be ready..."
    sleep 2
done

# Collect static files
./manage.py collectstatic --noinput

# Start Gunicorn
gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
