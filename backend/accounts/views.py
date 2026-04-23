"""
accounts views

Existing flows (login / logout) are preserved unchanged. The additions below
provide an admin-only in-app user management UI that wraps the existing User
model. No new fields, no migrations.
"""
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from mixins import AdminRequiredMixin
from .forms import UserAdminForm, SetPasswordForm
from .models import User


# ─── existing auth flows (unchanged behaviour) ──────────────────────────────
class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("accounts:login")


# ─── admin-only user management ─────────────────────────────────────────────
class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 25
    ordering = ["username"]


class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "viewed_user"


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserAdminForm
    template_name = "accounts/user_form.html"
    context_object_name = "viewed_user"

    def get_success_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f"Updated account: {form.instance.username}")
        return super().form_valid(form)


class UserPasswordResetView(AdminRequiredMixin, FormView):
    form_class = SetPasswordForm
    template_name = "accounts/user_password_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.target_user = User.objects.get(pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["viewed_user"] = self.target_user
        return ctx

    def form_valid(self, form):
        self.target_user.set_password(form.cleaned_data["password1"])
        self.target_user.save()
        messages.success(self.request,
                         f"Password updated for {self.target_user.username}.")
        return redirect("accounts:user_detail", pk=self.target_user.pk)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/user_confirm_delete.html"
    context_object_name = "viewed_user"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        # Refuse to delete the current admin to avoid lockout
        if self.object == self.request.user:
            messages.error(self.request, "You cannot delete your own account while signed in.")
            return redirect("accounts:user_detail", pk=self.object.pk)
        username = self.object.username
        response = super().form_valid(form)
        messages.success(self.request, f"Deleted account: {username}")
        return response
