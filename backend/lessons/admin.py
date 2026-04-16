from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "horse", "start_time", "status")
    list_filter = ("status",)
    search_fields = ("title",)
    filter_horizontal = ("members",)
