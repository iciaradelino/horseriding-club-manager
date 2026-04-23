# Backend additions for the role-aware dashboard

These six files are the only backend changes required to power the dashboards.
Already applied in the backend.zip you uploaded — included here for traceability
in case you want to re-deploy or review what differs from a vanilla backend.

| Path | Status | Why |
|---|---|---|
| `dashboard/views.py` | replaced | Role-dispatch + per-role aggregations |
| `dashboard/templatetags/__init__.py` | NEW | Empty package marker |
| `dashboard/templatetags/dashboard_extras.py` | NEW | Custom \|index & \|getitem filters |
| `accounts/views.py` | replaced | Adds 5 admin-only User CBVs (Login/LogoutView preserved) |
| `accounts/urls.py` | replaced | Adds 5 routes under accounts/users/... |
| `accounts/forms.py` | extended | Adds UserAdminForm + SetPasswordForm |

NO model changes. NO migrations. NO existing routes modified.
