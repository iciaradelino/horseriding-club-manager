from django.db import models
from django.conf import settings


class MembershipPlan(models.Model):
    class BillingCycle(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quarterly", "Quarterly"
        ANNUAL = "annual", "Annual"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_cycle = models.CharField(
        max_length=20, choices=BillingCycle.choices, default=BillingCycle.MONTHLY
    )
    lessons_per_cycle = models.PositiveIntegerField(
        null=True, blank=True, help_text="leave blank for unlimited"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_billing_cycle_display()})"


class Membership(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.member} — {self.plan.name}"


class Invoice(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"

    membership = models.ForeignKey(
        Membership, on_delete=models.CASCADE, related_name="invoices"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        ordering = ["-issued_date"]

    def __str__(self):
        return f"Invoice #{self.pk} — {self.membership.member} ({self.status})"
