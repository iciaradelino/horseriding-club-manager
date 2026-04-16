# Backend

## Structure

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── settings.py / urls.py / asgi.py / wsgi.py   ← project config
├── accounts/       custom user model + auth
├── members/        rider profiles
├── horses/         horse profiles + health records
├── lessons/        lesson scheduling
├── staff/          trainer profiles
├── billing/        membership plans, subscriptions, invoices
└── dashboard/      aggregated stats (no models)
```

---

## Design Decisions

**Custom User model (`accounts.User`)**
Extends `AbstractUser` with a `role` field (`admin`, `trainer`, `member`). Defined before any migrations — changing the auth model after the first migration is painful.

**Separated profile models**
`Member` and `Trainer` are `OneToOneField` profiles linked to `User`, not subclasses. Auth concerns stay in `accounts`; domain data stays in its own app.

**`Horse` + `HealthRecord` split**
Health history (vet/farrier visits, vaccinations) lives in a child `HealthRecord` model rather than fields on `Horse`, so records can accumulate over time.

**Billing chain: `MembershipPlan` → `Membership` → `Invoice`**
Plans are reusable templates. A `Membership` ties a member to a plan for a date range. `Invoice` records individual charges against a membership.

**`dashboard` has no models**
It queries other apps directly in `DashboardView.get_context_data`. No data duplication, no sync issues.

**Templates live in `frontend/templates/`**
`settings.py` points `TEMPLATES[0]["DIRS"]` at `../frontend/templates` so the backend and frontend stay in separate top-level folders.

---

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # fill in SECRET_KEY at minimum
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Environment Variables

| Variable        | Default                  | Notes                        |
|-----------------|--------------------------|------------------------------|
| `SECRET_KEY`    | —                        | required in production       |
| `DEBUG`         | `True`                   |                              |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost`    | comma-separated              |
| `DATABASE_URL`  | `sqlite:///db.sqlite3`   | switch to postgres in prod   |
