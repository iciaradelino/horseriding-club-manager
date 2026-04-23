"""
Role-aware dashboard.

This view dispatches to a different template fragment per user role and
provides each role with its own context. Everything is computed live from the
existing models — there are no new fields, no new tables, and no migrations.

Three role-specific contexts:
  * Admin   — club-wide health: counts, revenue, workload, alerts
  * Trainer — today's sessions, weekly schedule, busy-hours heatmap
  * Member  — own upcoming lessons, package usage, riding history
"""
import json
from datetime import date, datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.utils import timezone
from django.views.generic import TemplateView
from members.models import Member
from horses.models import Horse, HealthRecord
from lessons.models import Lesson
from staff.models import Trainer
from billing.models import Invoice, Membership


def _json(value):
    """Wrap a Python list/scalar as a JSON-encoded string for safe embedding
    into HTML data-* attributes."""
    return json.dumps(value)


# ─── helpers ───────────────────────────────────────────────────────────────
def _last_n_months(n=6):
    """Returns a list of (year, month, label) tuples for the last n months,
    oldest first, including the current month."""
    today = date.today()
    months = []
    y, m = today.year, today.month
    for _ in range(n):
        months.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    months.reverse()
    return [(y, m, date(y, m, 1).strftime("%b")) for y, m in months]


def _monthly_invoice_revenue(months):
    out = []
    for y, m, _ in months:
        total = (
            Invoice.objects
            .filter(status=Invoice.Status.PAID, paid_date__year=y, paid_date__month=m)
            .aggregate(total=Sum("amount"))["total"]
        )
        out.append(float(total or 0))
    return out


def _monthly_membership_counts(months):
    out = []
    for y, m, _ in months:
        out.append(
            Membership.objects.filter(start_date__year=y, start_date__month=m).count()
        )
    return out


# ─── view ──────────────────────────────────────────────────────────────────
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["now"] = timezone.now()

        # Cheap counts — used by header strip on every role's dashboard
        ctx["total_members"] = Member.objects.count()
        ctx["total_horses"] = Horse.objects.count()
        ctx["available_horses"] = Horse.objects.filter(status=Horse.Status.AVAILABLE).count()
        ctx["active_memberships"] = Membership.objects.filter(status=Membership.Status.ACTIVE).count()

        if user.is_admin:
            self._build_admin_context(ctx)
        elif user.is_trainer:
            self._build_trainer_context(ctx, user)
        elif user.is_member:
            self._build_member_context(ctx, user)

        return ctx

    # ─── ADMIN ────────────────────────────────────────────────────────────
    def _build_admin_context(self, ctx):
        now = ctx["now"]
        today = now.date()

        ctx["active_trainers"] = Trainer.objects.filter(is_active=True).count()
        ctx["pending_invoices"] = Invoice.objects.filter(status=Invoice.Status.PENDING).count()
        ctx["overdue_invoices"] = Invoice.objects.filter(status=Invoice.Status.OVERDUE).count()
        ctx["revenue_this_month"] = (
            Invoice.objects
            .filter(status=Invoice.Status.PAID, paid_date__month=now.month, paid_date__year=now.year)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        # 6-month series → bar charts (JSON-encoded for safe data-* embedding)
        months = _last_n_months(6)
        ctx["chart_months"]       = _json([m[2] for m in months])
        ctx["chart_revenue"]      = _json(_monthly_invoice_revenue(months))
        ctx["chart_memberships"]  = _json(_monthly_membership_counts(months))

        # Horse workload donut: count of all lessons per horse, top 8
        workload = (
            Lesson.objects
            .filter(horse__isnull=False)
            .values("horse__name")
            .annotate(total=Count("id"))
            .order_by("-total")[:8]
        )
        ctx["horse_workload_labels"] = _json([w["horse__name"] for w in workload])
        ctx["horse_workload_values"] = _json([w["total"] for w in workload])
        ctx["horse_workload_count"]  = len(workload)

        # Missing-payments table — overdue + pending, soonest due first
        ctx["overdue_invoice_rows"] = (
            Invoice.objects
            .filter(status__in=[Invoice.Status.OVERDUE, Invoice.Status.PENDING])
            .select_related("membership__member__user", "membership__plan")
            .order_by("due_date")[:10]
        )

        # Upcoming health events (vet, farrier, vaccination) within 60 days
        horizon = today + timedelta(days=60)
        ctx["upcoming_health_events"] = (
            HealthRecord.objects
            .filter(next_due_date__isnull=False,
                    next_due_date__gte=today,
                    next_due_date__lte=horizon)
            .select_related("horse")
            .order_by("next_due_date")[:10]
        )

        # Upcoming lessons preview
        ctx["upcoming_lessons"] = (
            Lesson.objects.filter(status=Lesson.Status.SCHEDULED, start_time__gte=now)
            .select_related("trainer__user", "horse")
            .order_by("start_time")[:5]
        )

    # ─── TRAINER ──────────────────────────────────────────────────────────
    def _build_trainer_context(self, ctx, user):
        now = ctx["now"]
        today = now.date()

        trainer = Trainer.objects.filter(user=user).first()
        ctx["trainer_profile"] = trainer
        if not trainer:
            return

        my_lessons_qs = Lesson.objects.filter(trainer=trainer).select_related("horse")

        # Sessions today
        start_of_day = datetime.combine(today, datetime.min.time(), tzinfo=now.tzinfo)
        end_of_day = start_of_day + timedelta(days=1)
        ctx["sessions_today"] = (
            my_lessons_qs.filter(start_time__gte=start_of_day, start_time__lt=end_of_day)
            .order_by("start_time")
            .prefetch_related("members__user")
        )

        # Weekly schedule (this Mon → next Mon)
        weekday_offset = today.weekday()  # mon=0
        week_start = today - timedelta(days=weekday_offset)
        week_end = week_start + timedelta(days=7)
        week_start_dt = datetime.combine(week_start, datetime.min.time(), tzinfo=now.tzinfo)
        week_end_dt = datetime.combine(week_end, datetime.min.time(), tzinfo=now.tzinfo)
        weekly = my_lessons_qs.filter(start_time__gte=week_start_dt,
                                      start_time__lt=week_end_dt).order_by("start_time")
        by_day = {i: [] for i in range(7)}
        for l in weekly:
            by_day[l.start_time.weekday()].append(l)
        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ctx["weekly_schedule"] = [
            {
                "name": weekday_names[i],
                "date": (week_start + timedelta(days=i)),
                "is_today": (week_start + timedelta(days=i)) == today,
                "lessons": by_day[i],
            }
            for i in range(7)
        ]

        # Recent activity — most recently created lessons assigned to me.
        # Lesson model has no edit history so we surface current status, not edits.
        ctx["recent_activity"] = my_lessons_qs.order_by("-id")[:8]

        # Heatmap matrix: 7 weekdays × 14 hours (06:00–19:00)
        sixty_days_ago = now - timedelta(days=60)
        recent = my_lessons_qs.filter(start_time__gte=sixty_days_ago)
        heat = [[0] * 14 for _ in range(7)]
        for l in recent:
            h = l.start_time.hour
            if 6 <= h <= 19:
                heat[l.start_time.weekday()][h - 6] += 1
        ctx["heatmap"] = heat
        ctx["heatmap_max"] = max((max(row) for row in heat), default=0)
        ctx["heatmap_hours"] = list(range(6, 20))
        ctx["heatmap_days"] = weekday_names

    # ─── MEMBER ───────────────────────────────────────────────────────────
    def _build_member_context(self, ctx, user):
        now = ctx["now"]

        member = Member.objects.filter(user=user).first()
        ctx["member_profile"] = member
        if not member:
            return

        my_lessons = Lesson.objects.filter(members=member).select_related("trainer__user", "horse")

        # Next 5 upcoming lessons
        upcoming = my_lessons.filter(start_time__gte=now,
                                     status=Lesson.Status.SCHEDULED).order_by("start_time")
        ctx["my_next_lessons"] = list(upcoming[:5])
        ctx["my_next_lesson"] = ctx["my_next_lessons"][0] if ctx["my_next_lessons"] else None

        # Active membership + remaining sessions in the cycle
        active_membership = (
            Membership.objects
            .filter(member=member, status=Membership.Status.ACTIVE)
            .select_related("plan")
            .order_by("-start_date")
            .first()
        )
        ctx["my_active_membership"] = active_membership
        if active_membership and active_membership.plan.lessons_per_cycle:
            used = my_lessons.filter(
                status=Lesson.Status.COMPLETED,
                start_time__date__gte=active_membership.start_date,
                start_time__date__lte=active_membership.end_date,
            ).count()
            ctx["sessions_used"] = used
            ctx["sessions_remaining"] = max(0, active_membership.plan.lessons_per_cycle - used)
            ctx["sessions_quota"] = active_membership.plan.lessons_per_cycle
        else:
            ctx["sessions_used"] = None
            ctx["sessions_remaining"] = None
            ctx["sessions_quota"] = None

        # Monthly activity bar chart (completed lessons per month, last 6 months)
        months = _last_n_months(6)
        activity_values = [
            my_lessons.filter(status=Lesson.Status.COMPLETED,
                              start_time__year=y, start_time__month=m).count()
            for y, m, _ in months
        ]
        ctx["activity_months"]     = _json([m[2] for m in months])
        ctx["activity_values"]     = _json(activity_values)
        ctx["activity_has_data"]   = any(activity_values)

        # Horse preference donut — counts of lessons-per-horse, last 12 months
        twelve_months_ago = now - timedelta(days=365)
        horse_counts = (
            my_lessons.filter(start_time__gte=twelve_months_ago, horse__isnull=False)
            .values("horse__name")
            .annotate(total=Count("id"))
            .order_by("-total")[:6]
        )
        ctx["horse_usage_labels"] = _json([h["horse__name"] for h in horse_counts])
        ctx["horse_usage_values"] = _json([h["total"] for h in horse_counts])
        ctx["horse_usage_count"]  = len(horse_counts)

        # Member's own outstanding invoices
        ctx["my_outstanding_invoices"] = (
            Invoice.objects
            .filter(membership__member=member,
                    status__in=[Invoice.Status.OVERDUE, Invoice.Status.PENDING])
            .select_related("membership__plan")
            .order_by("due_date")
        )
