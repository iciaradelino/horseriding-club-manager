from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from mixins import AdminRequiredMixin
from .models import MembershipPlan, Membership, Invoice
from .forms import MembershipForm, InvoiceForm, MarkPaidForm


class MembershipPlanListView(LoginRequiredMixin, ListView):
    model = MembershipPlan
    template_name = "billing/plan_list.html"
    context_object_name = "plans"
    queryset = MembershipPlan.objects.filter(is_active=True)


class MembershipListView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = "billing/membership_list.html"
    context_object_name = "memberships"
    queryset = Membership.objects.select_related("member__user", "plan")


class MembershipCreateView(AdminRequiredMixin, CreateView):
    model = Membership
    template_name = "billing/membership_form.html"
    form_class = MembershipForm
    success_url = reverse_lazy("billing:membership_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # auto-generate first invoice when membership is created
        membership = self.object
        Invoice.objects.create(
            membership=membership,
            amount=membership.plan.price,
            due_date=membership.start_date,
        )
        messages.success(self.request, "Membership created and first invoice generated.")
        return response


class MembershipUpdateView(AdminRequiredMixin, UpdateView):
    model = Membership
    template_name = "billing/membership_form.html"
    form_class = MembershipForm
    success_url = reverse_lazy("billing:membership_list")


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "billing/invoice_list.html"
    context_object_name = "invoices"
    queryset = Invoice.objects.select_related("membership__member__user", "membership__plan")


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "billing/invoice_detail.html"
    context_object_name = "invoice"
    queryset = Invoice.objects.select_related("membership__member__user", "membership__plan")


class InvoiceCreateView(AdminRequiredMixin, CreateView):
    model = Invoice
    template_name = "billing/invoice_form.html"
    form_class = InvoiceForm
    success_url = reverse_lazy("billing:invoice_list")


class InvoiceMarkPaidView(AdminRequiredMixin, UpdateView):
    model = Invoice
    template_name = "billing/invoice_mark_paid.html"
    form_class = MarkPaidForm

    def get_initial(self):
        return {"paid_date": date.today()}

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Invoice marked as paid.")
        return response

    def get_success_url(self):
        return reverse_lazy("billing:invoice_detail", kwargs={"pk": self.object.pk})
