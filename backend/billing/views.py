from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import MembershipPlan, Membership, Invoice


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


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "billing/invoice_list.html"
    context_object_name = "invoices"
    queryset = Invoice.objects.select_related("membership__member__user", "membership__plan")


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "billing/invoice_detail.html"
    context_object_name = "invoice"
