from django.db import models
from django.conf import settings


class Lesson(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=100)
    trainer = models.ForeignKey(
        "staff.Trainer",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lessons",
    )
    horse = models.ForeignKey(
        "horses.Horse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
    )
    members = models.ManyToManyField(
        "members.Member",
        related_name="lessons",
        blank=True,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.title} ({self.start_time:%Y-%m-%d %H:%M})"
