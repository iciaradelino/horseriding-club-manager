# Backend additions for the role-aware dashboard

You already applied all of these in your latest upload. Re-included here
for traceability. The one NEW thing worth noting: after this round the
frontend's dashboard.js now reliably renders charts even if Chart.js
loads slowly — see the frontend zip.

| Path | Status | Why |
|---|---|---|
| dashboard/views.py | replaced | Role-dispatch + per-role aggregations |
| dashboard/templatetags/__init__.py | NEW | Empty package marker |
| dashboard/templatetags/dashboard_extras.py | NEW | Custom \|index & \|getitem filters |
| dashboard/management/commands/seed.py | replaced | 6 months of history for full chart population |
| accounts/views.py | replaced | Admin-only User CBVs (Login/LogoutView preserved) |
| accounts/urls.py | replaced | Adds 5 routes under accounts/users/... |
| accounts/forms.py | extended | Adds UserAdminForm + SetPasswordForm |

NO model changes. NO migrations. NO existing routes modified.

# To see charts populated

  cd backend
  python manage.py seed
  python manage.py runserver

Log in as admin / admin1234 to see the monthly revenue bars rise across
November → April, etc. The seed command is idempotent-ish but the history
is built each time — if you get duplicates, reset with:
  rm backend/db.sqlite3
  python manage.py migrate
  python manage.py seed
