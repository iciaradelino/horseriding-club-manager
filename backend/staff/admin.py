from django.contrib import admin
from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "specialisation", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
