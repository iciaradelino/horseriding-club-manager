from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Lesson


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "lessons/lesson_list.html"
    context_object_name = "lessons"
    queryset = Lesson.objects.select_related("trainer__user", "horse")


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lessons/lesson_detail.html"
    context_object_name = "lesson"


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = "lessons/lesson_form.html"
    fields = ["title", "trainer", "horse", "members", "start_time", "end_time", "notes"]
    success_url = reverse_lazy("lessons:list")


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    template_name = "lessons/lesson_form.html"
    fields = ["title", "trainer", "horse", "members", "start_time", "end_time", "status", "notes"]
    success_url = reverse_lazy("lessons:list")
