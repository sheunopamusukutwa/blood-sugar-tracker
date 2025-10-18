#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🔧 Running database migrations..."
python manage.py migrate --noinput

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput