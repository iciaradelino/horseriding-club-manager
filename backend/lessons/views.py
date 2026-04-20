from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from mixins import AdminOrTrainerMixin
from .models import Lesson
from .forms import LessonForm


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "lessons/lesson_list.html"
    context_object_name = "lessons"
    queryset = Lesson.objects.select_related("trainer__user", "horse")


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lessons/lesson_detail.html"
    context_object_name = "lesson"
    queryset = Lesson.objects.select_related("trainer__user", "horse").prefetch_related("members__user")


class LessonCreateView(AdminOrTrainerMixin, CreateView):
    model = Lesson
    template_name = "lessons/lesson_form.html"
    form_class = LessonForm
    success_url = reverse_lazy("lessons:list")


class LessonUpdateView(AdminOrTrainerMixin, UpdateView):
    model = Lesson
    template_name = "lessons/lesson_form.html"
    form_class = LessonForm
    success_url = reverse_lazy("lessons:list")
