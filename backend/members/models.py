from django.db import models
from django.conf import settings


class Member(models.Model):
    class SkillLevel(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="member_profile",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    skill_level = models.CharField(
        max_length=20, choices=SkillLevel.choices, default=SkillLevel.BEGINNER
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
