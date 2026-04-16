from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Trainer


class TrainerListView(LoginRequiredMixin, ListView):
    model = Trainer
    template_name = "staff/trainer_list.html"
    context_object_name = "trainers"
    queryset = Trainer.objects.filter(is_active=True).select_related("user")


class TrainerDetailView(LoginRequiredMixin, DetailView):
    model = Trainer
    template_name = "staff/trainer_detail.html"
    context_object_name = "trainer"


class TrainerCreateView(LoginRequiredMixin, CreateView):
    model = Trainer
    template_name = "staff/trainer_form.html"
    fields = ["user", "specialisation", "bio"]
    success_url = reverse_lazy("staff:list")


class TrainerUpdateView(LoginRequiredMixin, UpdateView):
    model = Trainer
    template_name = "staff/trainer_form.html"
    fields = ["specialisation", "bio", "is_active"]
    success_url = reverse_lazy("staff:list")
