# Blood Sugar Tracker API (Django + DRF)

A minimal REST API for recording and viewing personal blood glucose readings. Built as an ALX Backend capstone.

> **Status:** MVP in progress (Part 4). Token auth + CRUD + filtering/ordering are live.

---

## ✨ Features (current)
- **Auth**
  - User **register** & **login** (returns DRF **Token**)
  - **Profile**: get/update current user
- **Readings**
  - **CRUD** scoped to the authenticated user
  - **Filtering**: `date_from`, `date_to`, `status`
  - **Ordering**: `?ordering=timestamp` or `?ordering=-timestamp` (default newest first). Also `value`, `status`
  - **Pagination**: page size = 20 (configurable)
- **Utility**
  - JSON landing at `/` listing endpoints
  - Health check at `/healthz`

---

## 🧱 Stack
- Python 3.11+
- Django 5.2.x
- Django REST Framework
- django-filter
- SQLite (dev)

---

## 🚀 Quickstart

```bash
# 1) Clone
git clone https://github.com/sheunopamusukutwa/blood-sugar-tracker.git
cd blood-sugar-tracker

# 2) Virtualenv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt  # if missing, install: django djangorestframework django-filter

# 4) (Optional) Environment
# Create .env and set values as needed
# DJANGO_SECRET_KEY=dev-secret-key
# DJANGO_DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1
# PAGE_SIZE=20
# TIME_ZONE=UTC

# 5) DB setup
python manage.py migrate
python manage.py createsuperuser  # optional (for admin/inspection)

# 6) Run
python manage.py runserver
# → http://127.0.0.1:8000/
```

---

## 🔌 Endpoints

Base URL (local): `http://127.0.0.1:8000`

### Utility
| Method | Path         | Description                    |
|-------:|--------------|--------------------------------|
| GET    | `/`          | API root (JSON with links)     |
| GET    | `/healthz`   | Health probe                   |

### Auth & Profile
| Method | Path            | Body / Notes                                  |
|-------:|------------------|-----------------------------------------------|
| POST   | `/api/register/` | `{"username":"...", "password":"..."}`      |
| POST   | `/api/login/`    | Returns `{"token": "<DRF token>"}`          |
| GET    | `/api/profile/`  | Requires `Authorization: Token <token>`       |
| PUT    | `/api/profile/`  | Partial update of current user fields         |

**Auth header:**  
`Authorization: Token <your-token>`

### Readings
| Method | Path                         | Notes |
|-------:|------------------------------|-------|
| GET    | `/api/readings/`             | List (auth required) |
| POST   | `/api/readings/`             | Create (auth required) |
| GET    | `/api/readings/<id>/`        | Retrieve (auth required) |
| PUT    | `/api/readings/<id>/`        | Update (auth required) |
| PATCH  | `/api/readings/<id>/`        | Partial update (auth required) |
| DELETE | `/api/readings/<id>/`        | Delete (auth required) |

**Reading fields (example)**  
```json
{
  "id": 1,
  "timestamp": "2025-10-11T18:30:00Z",
  "value": 6.2,
  "unit": "mmol/L",
  "status": "fasting",
  "notes": "evening check"
}
```

---

## 🔎 Filtering & Ordering

Enabled on `GET /api/readings/`:

**Filters**
- `date_from=YYYY-MM-DD` (inclusive; compares against the DATE part of `timestamp`)
- `date_to=YYYY-MM-DD` (inclusive)
- `status=<fasting|random|postprandial>` (case-insensitive)

**Ordering**
- `ordering=timestamp` → oldest → newest
- `ordering=-timestamp` → newest → oldest (**default**)
- Also supported: `value`, `-value`, `status`, `-status`

**Examples**
```bash
# List newest first (default)
curl -s "http://127.0.0.1:8000/api/readings/" -H "Authorization: Token $TOKEN"

# Date range
curl -s "http://127.0.0.1:8000/api/readings/?date_from=2025-10-01&date_to=2025-10-11"   -H "Authorization: Token $TOKEN"

# Status only
curl -s "http://127.0.0.1:8000/api/readings/?status=fasting"   -H "Authorization: Token $TOKEN"

# Oldest → newest
curl -s "http://127.0.0.1:8000/api/readings/?ordering=timestamp"   -H "Authorization: Token $TOKEN"
```

---

## 🧪 Quick cURL Flow

```bash
# 1) Register
curl -s -X POST http://127.0.0.1:8000/api/register/   -H "Content-Type: application/json"   -d '{"username":"demo","password":"DemoPass123"}'

# 2) Login (capture token)
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/login/   -H "Content-Type: application/json"   -d '{"username":"demo","password":"DemoPass123"}' | python - <<'PY'
import sys, json; print(json.load(sys.stdin)["token"])
PY
)

# 3) Create a reading
curl -s -X POST http://127.0.0.1:8000/api/readings/   -H "Authorization: Token $TOKEN" -H "Content-Type: application/json"   -d '{"timestamp":"2025-10-11T18:30:00Z","value":6.2,"status":"fasting","unit":"mmol/L","notes":"evening"}'

# 4) List with filters
curl -s "http://127.0.0.1:8000/api/readings/?date_from=2025-10-01&status=fasting&ordering=-timestamp"   -H "Authorization: Token $TOKEN"
```

---

## ⚙️ Configuration

`config/settings.py` reads some environment variables (all optional for local dev):

| Variable           | Default | Purpose |
|--------------------|---------|---------|
| `DJANGO_SECRET_KEY`| dev key | Security key (set a real one in prod) |
| `DJANGO_DEBUG`     | `True`  | Turn off in prod |
| `ALLOWED_HOSTS`    | `*` in DEBUG | Comma-separated list in prod |
| `PAGE_SIZE`        | `20`    | DRF pagination |
| `TIME_ZONE`        | `UTC`   | Server/app timezone |

---

## 📁 Project Structure (high level)
```
config/
  settings.py
  urls.py
  wsgi.py
tracker/
  models.py
  serializers.py
  views.py
manage.py
README.md
requirements.txt
```

---

## 🧭 Roadmap (next)
- OpenAPI + Swagger UI (`drf-spectacular`) at `/api/docs/`
- CSV export/import for readings
- Summary/analytics endpoint (avg/min/max, % in range)
- Basic CI (GitHub Actions) to run tests on push

---

## 📝 Notes
- This API is not yet hardened for production (e.g., rate limiting, CORS, HTTPS, secure secrets). For learning/demo use.
- Remember to keep the repo **public** for review during the capstone.

---

## 📜 License
TBD (add a `LICENSE` file — MIT recommended for educational projects).
