from datetime import date
from dateutil.relativedelta import relativedelta
from django import forms
from .models import MembershipPlan, Membership, Invoice


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ["member", "plan", "start_date", "end_date", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        plan = cleaned.get("plan")
        start = cleaned.get("start_date")

        # auto-compute end_date if omitted
        if plan and start and not cleaned.get("end_date"):
            cycle = plan.billing_cycle
            if cycle == MembershipPlan.BillingCycle.MONTHLY:
                cleaned["end_date"] = start + relativedelta(months=1)
            elif cycle == MembershipPlan.BillingCycle.QUARTERLY:
                cleaned["end_date"] = start + relativedelta(months=3)
            elif cycle == MembershipPlan.BillingCycle.ANNUAL:
                cleaned["end_date"] = start + relativedelta(years=1)

        return cleaned


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["membership", "amount", "due_date", "status"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class MarkPaidForm(forms.ModelForm):
    """minimal form used by the mark-as-paid view."""

    class Meta:
        model = Invoice
        fields = ["paid_date"]
        widgets = {
            "paid_date": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        invoice = super().save(commit=False)
        invoice.status = Invoice.Status.PAID
        if not invoice.paid_date:
            invoice.paid_date = date.today()
        if commit:
            invoice.save()
        return invoice
