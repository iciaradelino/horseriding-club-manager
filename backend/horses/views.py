from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Horse, HealthRecord


class HorseListView(LoginRequiredMixin, ListView):
    model = Horse
    template_name = "horses/horse_list.html"
    context_object_name = "horses"


class HorseDetailView(LoginRequiredMixin, DetailView):
    model = Horse
    template_name = "horses/horse_detail.html"
    context_object_name = "horse"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["health_records"] = self.object.health_records.all()
        return ctx


class HorseCreateView(LoginRequiredMixin, CreateView):
    model = Horse
    template_name = "horses/horse_form.html"
    fields = ["name", "breed", "date_of_birth", "color", "status", "notes", "photo"]
    success_url = reverse_lazy("horses:list")


class HorseUpdateView(LoginRequiredMixin, UpdateView):
    model = Horse
    template_name = "horses/horse_form.html"
    fields = ["name", "breed", "date_of_birth", "color", "status", "notes", "photo"]
    success_url = reverse_lazy("horses:list")


class HealthRecordCreateView(LoginRequiredMixin, CreateView):
    model = HealthRecord
    template_name = "horses/health_record_form.html"
    fields = ["record_type", "date", "description", "performed_by", "next_due_date"]

    def form_valid(self, form):
        form.instance.horse_id = self.kwargs["horse_pk"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("horses:detail", kwargs={"pk": self.kwargs["horse_pk"]})
