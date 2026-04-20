from django import forms
from django.db import transaction
from accounts.models import User
from accounts.forms import UserProfileForm
from .models import Trainer


class TrainerRegistrationForm(UserProfileForm):
    """creates a User(role=trainer) and a Trainer profile in one transaction."""

    specialisation = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))

    @transaction.atomic
    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data.get("first_name", ""),
            last_name=self.cleaned_data.get("last_name", ""),
            email=self.cleaned_data.get("email", ""),
            phone=self.cleaned_data.get("phone", ""),
            role=User.Role.TRAINER,
        )
        user.set_password(self.cleaned_data["password1"])
        user.save()

        trainer = Trainer(
            user=user,
            specialisation=self.cleaned_data.get("specialisation", ""),
            bio=self.cleaned_data.get("bio", ""),
        )
        trainer.save()
        return trainer


class TrainerUpdateForm(forms.ModelForm):
    """updates trainer profile fields only."""

    class Meta:
        model = Trainer
        fields = ["specialisation", "bio", "is_active"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
