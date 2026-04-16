from django.contrib import admin
from .models import MembershipPlan, Membership, Invoice


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "billing_cycle", "price", "is_active")
    list_filter = ("billing_cycle", "is_active")


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    readonly_fields = ("issued_date",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("member", "plan", "start_date", "end_date", "status")
    list_filter = ("status", "plan")
    inlines = [InvoiceInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("__str__", "amount", "due_date", "status")
    list_filter = ("status",)
