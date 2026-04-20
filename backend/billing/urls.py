from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("plans/", views.MembershipPlanListView.as_view(), name="plan_list"),
    path("memberships/", views.MembershipListView.as_view(), name="membership_list"),
    path("memberships/add/", views.MembershipCreateView.as_view(), name="membership_create"),
    path("memberships/<int:pk>/edit/", views.MembershipUpdateView.as_view(), name="membership_update"),
    path("invoices/", views.InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/add/", views.InvoiceCreateView.as_view(), name="invoice_create"),
    path("invoices/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("invoices/<int:pk>/pay/", views.InvoiceMarkPaidView.as_view(), name="invoice_pay"),
]
