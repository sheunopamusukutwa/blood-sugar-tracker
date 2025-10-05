This is a Blood Sugar Level Tracker API. It is an API built with Django REST Framework that lets users record, manage, and analyze their blood sugar readings.

High-Level Features:

- Register and login users
- Add, update, delete, and list readings
- Manage profile info
- Token authentication

Endpoints

POST `/api/auth/register/` Register new user
POST `/api/auth/login/` Login user and return token
GET `/api/readings/` List readings
POST `/api/readings/` Add reading
GET `/api/readings/{id}/` View single reading
PUT `/api/readings/{id}/` Update reading
DELETE `/api/readings/{id}/` Delete reading
GET `/api/profile/` View profile
PUT `/api/profile/` Update profile

Setup

```bash
git clone https://github.com/<username>/blood-sugar-tracker.git
cd blood-sugar-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver