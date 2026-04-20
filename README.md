# Horse Riding Club Manager

A Django web application for managing the daily operations of a horse riding club.

---

## Features

- **Authentication & roles** — login, permissions, and role-based access (admin, trainer, member)
- **Dashboard** — overview with key stats and data analytics
- **Rider management** — track member profiles, skill levels, and history
- **Horse management** — horse profiles, health records, and assignment tracking
- **Lesson management** — schedule and manage lessons, assign horses and trainers
- **Trainer/staff management** — staff profiles, availability, and assignments
- **Membership management** — membership tiers, renewals, and billing??
- **Calendar** — unified view of lessons, events, vet visits, and farrier appointments

---

## Tech Stack

- **Backend:** Python / Django
- **Frontend:** HTML, Django Templates, Tailwind CSS
- **Database:** PostgreSQL ??

---

## Project Structure

```
horseriding-club-manager/
│
├── backend/                    # django project root
│   ├── manage.py
│   ├── requirements.txt
│   │
│   ├── horse_club_admin/       # django settings & config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── accounts/               # authentication, roles, permissions
│   ├── members/                # rider/member profiles
│   ├── horses/                 # horse profiles and health records
│   ├── lessons/                # lesson scheduling and management
│   ├── staff/                  # trainer and staff management
│   ├── billing/                # membership plans and payments
│   └── dashboard/              # aggregated stats and analytics
│
├── frontend/                   # static assets and templates
│   ├── templates/
│   │   ├── base.html
│   │   ├── accounts/
│   │   ├── members/
│   │   ├── horses/
│   │   ├── lessons/
│   │   ├── staff/
│   │   ├── billing/
│   │   └── dashboard/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
└── README.md
```

---
