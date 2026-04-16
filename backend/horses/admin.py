from django.contrib import admin
from .models import Horse, HealthRecord


class HealthRecordInline(admin.TabularInline):
    model = HealthRecord
    extra = 0


@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "status", "age")
    list_filter = ("status",)
    search_fields = ("name", "breed")
    inlines = [HealthRecordInline]


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ("horse", "record_type", "date", "performed_by", "next_due_date")
    list_filter = ("record_type",)
