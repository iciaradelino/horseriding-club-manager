from django.db import models


class Horse(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        IN_LESSON = "in_lesson", "In Lesson"
        RESTING = "resting", "Resting"
        RETIRED = "retired", "Retired"

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to="horses/", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class HealthRecord(models.Model):
    class RecordType(models.TextChoices):
        VET = "vet", "Vet Visit"
        FARRIER = "farrier", "Farrier Visit"
        VACCINATION = "vaccination", "Vaccination"
        OTHER = "other", "Other"

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name="health_records")
    record_type = models.CharField(max_length=20, choices=RecordType.choices)
    date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=100, blank=True)
    next_due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.horse.name} — {self.get_record_type_display()} ({self.date})"
