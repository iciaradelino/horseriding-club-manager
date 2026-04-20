from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from mixins import AdminRequiredMixin
from .models import Member
from .forms import MemberRegistrationForm, MemberUpdateForm, UserInlineForm


class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = "members/member_list.html"
    context_object_name = "members"
    queryset = Member.objects.select_related("user")


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = "members/member_detail.html"
    context_object_name = "member"

    def get_queryset(self):
        qs = super().get_queryset().select_related("user")
        # members can only view their own profile
        user = self.request.user
        if user.is_member:
            return qs.filter(user=user)
        return qs

    pass


class MemberCreateView(AdminRequiredMixin, CreateView):
    template_name = "members/member_form.html"
    form_class = MemberRegistrationForm
    success_url = reverse_lazy("members:list")

    def form_valid(self, form):
        form.save()
        from django.contrib import messages
        messages.success(self.request, "Member created successfully.")
        from django.shortcuts import redirect
        return redirect(self.success_url)


class MemberUpdateView(AdminRequiredMixin, UpdateView):
    model = Member
    template_name = "members/member_form.html"
    form_class = MemberUpdateForm
    success_url = reverse_lazy("members:list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            ctx["user_form"] = UserInlineForm(self.request.POST, instance=self.object.user)
        else:
            ctx["user_form"] = UserInlineForm(instance=self.object.user)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        user_form = ctx["user_form"]
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)
