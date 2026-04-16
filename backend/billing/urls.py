from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("plans/", views.MembershipPlanListView.as_view(), name="plan_list"),
    path("memberships/", views.MembershipListView.as_view(), name="membership_list"),
    path("invoices/", views.InvoiceListView.as_view(), name="invoice_list"),
    path("invoices/<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
]
