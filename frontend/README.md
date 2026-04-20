# Herradura — Frontend

The front-of-house for the Horseriding Club Manager. Every template, stylesheet
and asset the Django project renders lives in this folder.

---

## The stack

| Layer | Choice |
| --- | --- |
| Templates | **Django Templates** (`frontend/templates/`) — server-rendered; this is a classic Django MVT app, not an SPA |
| Styling | **Tailwind CSS** via Play CDN + a custom design system in `static/css/app.css` |
| Interactivity | **Alpine.js** for small local state — filter toggles, sidebar, mobile nav, inline-computed dashboard totals |
| Charts | **Chart.js** for the dashboard's horse-utilisation donut (real data from backend context) |
| Fonts | Fraunces (display), Geist (body), Geist Mono (numerics) via Google Fonts |

Everything is loaded via CDN so there is **no Node.js build step**. `python manage.py runserver` is all the team needs.

> **Note on Tailwind Play CDN**: fine for development and a classroom demo.
> For a real production deployment, compile Tailwind once with the standalone
> CLI into `static/css/tailwind.css` and drop the `cdn.tailwindcss.com`
> script tag from `base.html`.

---

## Setup

1. Install Python dependencies: `pip install -r backend/requirements.txt`.
2. Run migrations: `python backend/manage.py makemigrations && python backend/manage.py migrate`.
3. Create a superuser: `python backend/manage.py createsuperuser`.
4. Start the dev server: `python backend/manage.py runserver`.

The template and static directories are already wired up in `backend/settings.py`:

```python
"DIRS": [BASE_DIR.parent / "frontend" / "templates"]
STATICFILES_DIRS = [BASE_DIR.parent / "frontend" / "static"]
```

No additional configuration needed.

---

## File layout

```
frontend/
├── static/
│   ├── css/app.css            Design system: tokens, components, forms, print
│   ├── js/app.js              Global: sidebar, toast dismiss, date input upgrade
│   ├── js/dashboard.js        Chart.js setup for the horse-utilisation donut
│   └── img/logo.svg
│
└── templates/
    ├── base.html              App shell: sidebar, topbar, fonts, scripts
    ├── 404.html, 500.html
    ├── partials/
    │   ├── _form.html         Reusable Django form renderer
    │   ├── _empty.html        Empty-state card for lists with no records
    │   └── _messages.html     Toast notifications (Django messages framework)
    ├── accounts/              login
    ├── dashboard/             stats + horse utilisation + alerts + upcoming lessons
    ├── members/               riders list / detail / form
    ├── horses/                list / detail / form + health records
    ├── lessons/               list / detail / form
    ├── staff/                 trainers list / detail / form
    └── billing/               plans, memberships, invoices
```

---

## Design system

Defined as CSS variables in `static/css/app.css`:

- **Palette**: `--color-primary` (deep forest green), `--color-accent` (antique brass), `--color-paper` (warm cream), `--color-ink` (near-black)
- **Typography**: Fraunces / Geist / Geist Mono
- **Components**: `.btn`, `.card`, `.stat`, `.table-wrap`, `.badge`, `.form`, `.empty`, `.horse-card`
- **Utilities**: `.grid-2`, `.grid-3`, `.grid-4`, `.grid-auto`, `.flex`, `.tabular`, `.fade-in`, `.stagger`

Changing one CSS variable updates every surface consistently.

---

## What the dashboard shows

The dashboard is honest about what the backend actually surfaces today. It
renders only values that `DashboardView.get_context_data` provides:

| Section | Source |
| --- | --- |
| "Total Riders" stat | `total_members` |
| "Horses on Roll" + in-service count | `total_horses`, `available_horses` (difference computed client-side with Alpine) |
| "Upcoming Lessons" stat | `upcoming_lessons\|length` |
| "Billing Alerts" stat | `pending_invoices + overdue_invoices` |
| "Horse availability" donut | `data-total` / `data-available` on the canvas |
| "Things to action" panel | `pending_invoices`, `overdue_invoices` |
| "Next five lessons" list | `upcoming_lessons` queryset |

If the backend context is later extended with real aggregations (revenue,
lessons trend, skill distribution), additional charts can be added — the
shell in the charts row is ready.

---

## Messages

Any view that uses Django's `messages.success(request, "...")` /
`messages.error(...)` renders as a toast in the bottom-right corner,
coloured by the message tag. Already wired in `base.html`.

---

## Browser support

Anything released in the last two years. Uses modern CSS (`grid`, custom
properties, `aspect-ratio`, backdrop filters) and ES6+ JavaScript.

---

## What is deliberately *not* here

- **No Node.js / npm build step** — Tailwind via CDN keeps setup to `pip install` + `runserver`
- **No JSON API layer** — backend renders templates directly; there is no `fetch`/`axios` anywhere in the frontend
- **No new Python dependencies** — forms render through Django's default field loop, styled via CSS selectors on the underlying `<input>`/`<select>`/`<textarea>`
- **No service worker / PWA manifest** — out of scope
