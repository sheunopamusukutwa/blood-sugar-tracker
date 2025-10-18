#!/usr/bin/env zsh
# Dev setup helper for macOS (zsh)
# Usage: ./dev_setup.sh

set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR"

VENV_DIR=.venv

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  echo "Created virtualenv at $VENV_DIR"
fi

# Activate venv for the current shell
source "$VENV_DIR/bin/activate"

echo "Installing development requirements..."
pip install -U pip setuptools wheel
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Django development server in background (nohup). Logs: devserver.log"
# Start server in background and detach using nohup so it keeps running after the script exits
nohup python manage.py runserver 0.0.0.0:8000 > devserver.log 2>&1 &

echo "Server started (background). Use 'tail -f devserver.log' to view output."
