from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from members.models import Member
from horses.models import Horse
from lessons.models import Lesson
from billing.models import Invoice


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total_members"] = Member.objects.count()
        ctx["total_horses"] = Horse.objects.count()
        ctx["available_horses"] = Horse.objects.filter(status=Horse.Status.AVAILABLE).count()
        ctx["upcoming_lessons"] = (
            Lesson.objects.filter(status=Lesson.Status.SCHEDULED)
            .select_related("trainer__user", "horse")
            .order_by("start_time")[:5]
        )
        ctx["pending_invoices"] = Invoice.objects.filter(status=Invoice.Status.PENDING).count()
        ctx["overdue_invoices"] = Invoice.objects.filter(status=Invoice.Status.OVERDUE).count()
        return ctx
