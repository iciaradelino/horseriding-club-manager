from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from members.models import Member
from horses.models import Horse
from lessons.models import Lesson
from billing.models import Invoice, Membership


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()

        ctx["total_members"] = Member.objects.count()
        ctx["total_horses"] = Horse.objects.count()
        ctx["available_horses"] = Horse.objects.filter(status=Horse.Status.AVAILABLE).count()
        ctx["active_memberships"] = Membership.objects.filter(status=Membership.Status.ACTIVE).count()

        ctx["upcoming_lessons"] = (
            Lesson.objects.filter(status=Lesson.Status.SCHEDULED)
            .select_related("trainer__user", "horse")
            .order_by("start_time")[:5]
        )

        ctx["pending_invoices"] = Invoice.objects.filter(status=Invoice.Status.PENDING).count()
        ctx["overdue_invoices"] = Invoice.objects.filter(status=Invoice.Status.OVERDUE).count()

        revenue = (
            Invoice.objects
            .filter(status=Invoice.Status.PAID, paid_date__month=now.month, paid_date__year=now.year)
            .aggregate(total=Sum("amount"))["total"]
        )
        ctx["revenue_this_month"] = revenue or 0

        return ctx
