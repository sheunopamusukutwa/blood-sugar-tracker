#!/usr/bin/env bash
# Exit on error

set -o errexit

# Install deps (Render won't do this if we override the build command)
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "🔧 Running database migrations..."
python manage.py migrate --noinput

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput