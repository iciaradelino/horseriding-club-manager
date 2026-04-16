from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("__str__", "skill_level", "joined_date")
    list_filter = ("skill_level",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
