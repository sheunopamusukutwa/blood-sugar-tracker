# Blood Sugar Level Tracker API

This is a Blood Sugar Level Tracker API built with Django REST Framework that lets users record, manage, and analyze their blood sugar readings.

High-Level Features

- Register and login users
- Add, update, delete, and list readings
- Manage profile info
- Token authentication

API Endpoints

- POST `/api/auth/register/` — Register new user
- POST `/api/auth/login/` — Login user and return token
- GET `/api/readings/` — List readings
- POST `/api/readings/` — Add reading
- GET `/api/readings/{id}/` — View single reading
- PUT `/api/readings/{id}/` — Update reading
- DELETE `/api/readings/{id}/` — Delete reading
- GET `/api/profile/` — View profile
- PUT `/api/profile/` — Update profile

Quick Setup

```bash
git clone https://github.com/sheunopamusukutwa/blood-sugar-tracker.git
cd blood-sugar-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Local macOS development (fast, SQLite)

If you want a quick local development setup that uses SQLite (no Postgres required), a helper script is included to automate venv creation, install dev dependencies, migrate and start the dev server in the background.

```bash
cd blood-sugar-tracker
chmod +x dev_setup.sh
./dev_setup.sh
tail -f devserver.log
```

Notes

- `dev_setup.sh` installs `requirements-dev.txt` (this excludes `psycopg2-binary`) so you don't need `pg_config` or Postgres locally.
- If you intend to use Postgres locally or for deployment (Heroku), install PostgreSQL's client tools first so `pg_config` is available:

```bash
brew install postgresql
source .venv/bin/activate
pip install -r requirements.txt
```

- API root when running locally: `http://127.0.0.1:8000/api/`.

Development files added

- `requirements-dev.txt` — development-only dependencies (no `psycopg2-binary`)
- `dev_setup.sh` — helper script to create `.venv`, install dev deps, run migrations and start dev server (logs to `devserver.log`)

If you'd like, I can (A) push these changes to the repository, (B) add more tests, or (C) add a Makefile to standardize common developer commands. Tell me which you prefer.