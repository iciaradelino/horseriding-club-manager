from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Member


class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = "members/member_list.html"
    context_object_name = "members"


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = "members/member_detail.html"
    context_object_name = "member"


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    template_name = "members/member_form.html"
    fields = ["skill_level", "date_of_birth", "emergency_contact_name", "emergency_contact_phone", "notes"]
    success_url = reverse_lazy("members:list")


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = "members/member_form.html"
    fields = ["skill_level", "date_of_birth", "emergency_contact_name", "emergency_contact_phone", "notes"]
    success_url = reverse_lazy("members:list")
