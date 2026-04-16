from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        TRAINER = "trainer", "Trainer"
        MEMBER = "member", "Member"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_trainer(self):
        return self.role == self.Role.TRAINER

    @property
    def is_member(self):
        return self.role == self.Role.MEMBER
