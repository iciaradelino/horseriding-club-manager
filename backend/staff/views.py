from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from mixins import AdminRequiredMixin
from .models import Trainer
from .forms import TrainerRegistrationForm, TrainerUpdateForm


class TrainerListView(LoginRequiredMixin, ListView):
    model = Trainer
    template_name = "staff/trainer_list.html"
    context_object_name = "trainers"
    queryset = Trainer.objects.filter(is_active=True).select_related("user")


class TrainerDetailView(LoginRequiredMixin, DetailView):
    model = Trainer
    template_name = "staff/trainer_detail.html"
    context_object_name = "trainer"
    queryset = Trainer.objects.select_related("user")

    pass


class TrainerCreateView(AdminRequiredMixin, CreateView):
    template_name = "staff/trainer_form.html"
    form_class = TrainerRegistrationForm
    success_url = reverse_lazy("staff:list")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Trainer created successfully.")
        return redirect(self.success_url)


class TrainerUpdateView(AdminRequiredMixin, UpdateView):
    model = Trainer
    template_name = "staff/trainer_form.html"
    form_class = TrainerUpdateForm
    success_url = reverse_lazy("staff:list")
