# Backend

## Structure

```
backend/
├── manage.py
├── requirements.txt
├── .env.example
├── mixins.py               ← shared RBAC mixins (AdminRequiredMixin, AdminOrTrainerMixin)
├── settings.py / urls.py / asgi.py / wsgi.py   ← project config
├── accounts/               custom user model + auth, UserProfileForm base
├── members/                rider profiles, MemberRegistrationForm, MemberUpdateForm
├── horses/                 horse profiles + health records, HorseForm, HealthRecordForm
├── lessons/                lesson scheduling, LessonForm (datetime-local widgets)
├── staff/                  trainer profiles, TrainerRegistrationForm, TrainerUpdateForm
├── billing/                plans, memberships, invoices + mark-as-paid workflow
└── dashboard/              aggregated stats (no models) + seed management command
    └── management/
        └── commands/
            └── seed.py     ← populates the db with sample data
```

---

## Design Decisions

**Custom User model (`accounts.User`)**
Extends `AbstractUser` with a `role` field (`admin`, `trainer`, `member`). Defined before any migrations — changing the auth model after the first migration is painful.

**Separated profile models**
`Member` and `Trainer` are `OneToOneField` profiles linked to `User`, not subclasses. Auth concerns stay in `accounts`; domain data stays in its own app.

**Combined registration forms**
`MemberRegistrationForm` and `TrainerRegistrationForm` create a `User` + profile in a single `db.transaction.atomic` call. The `user` field is never exposed as a raw dropdown.

**`Horse` + `HealthRecord` split**
Health history (vet/farrier visits, vaccinations) lives in a child `HealthRecord` model rather than fields on `Horse`, so records can accumulate over time.

**Billing chain: `MembershipPlan` → `Membership` → `Invoice`**
Plans are reusable templates. A `Membership` ties a member to a plan for a date range. `Invoice` records individual charges against a membership. Creating a membership auto-generates the first invoice.

**Role-based access control via mixins**
`AdminRequiredMixin` (all create/update views) and `AdminOrTrainerMixin` (lesson and health record create/update) extend `UserPassesTestMixin` and live in `backend/mixins.py` so every app can import them without circular dependencies.

**`dashboard` has no models**
It queries other apps directly in `DashboardView.get_context_data`. Surfaces: total members, total/available horses, active memberships, upcoming lessons, pending/overdue invoices, and revenue this month.

**Templates live in `frontend/templates/`**
`settings.py` points `TEMPLATES[0]["DIRS"]` at `../frontend/templates` so the backend and frontend stay in separate top-level folders.

---

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in SECRET_KEY at minimum
python manage.py migrate
python manage.py runserver
```

To populate the database with sample data instead of starting empty:

```bash
python manage.py seed
```

This creates 1 admin, 3 trainers, 10 members, 6 horses, 5 membership plans, and 20 lessons.

| Seeded account | Password | Role |
|---|---|---|
| `admin` | `admin1234` | Admin (+ Django admin access) |
| `sophia_trainer`, `james_trainer`, `elena_trainer` | `trainer1234` | Trainer |
| `alice_m` … `jack_m` | `member1234` | Member |

---

## URL Structure

| Prefix | App | Notes |
|---|---|---|
| `/` | dashboard | home stats view |
| `/accounts/` | accounts | login / logout |
| `/members/` | members | list, detail, add, edit |
| `/horses/` | horses | list, detail, add, edit, health record add |
| `/lessons/` | lessons | list (+ FullCalendar), detail, add, edit |
| `/staff/` | staff | trainer list, detail, add, edit |
| `/billing/plans/` | billing | plan list (read-only; manage via admin) |
| `/billing/memberships/` | billing | list, add, edit |
| `/billing/invoices/` | billing | list, add, detail, mark-as-paid |
| `/admin/` | Django admin | full model access |

---

## Environment Variables

| Variable        | Default                | Notes                      |
|-----------------|------------------------|----------------------------|
| `SECRET_KEY`    | —                      | required in production     |
| `DEBUG`         | `True`                 |                            |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost`  | comma-separated            |
| `DATABASE_URL`  | `sqlite:///db.sqlite3` | switch to postgres in prod |
