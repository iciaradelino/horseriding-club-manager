from django import forms
from django.db import transaction
from accounts.models import User
from accounts.forms import UserProfileForm
from .models import Member


class MemberRegistrationForm(UserProfileForm):
    """creates a User(role=member) and a Member profile in one transaction."""

    skill_level = forms.ChoiceField(choices=Member.SkillLevel.choices)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    emergency_contact_name = forms.CharField(max_length=100, required=False)
    emergency_contact_phone = forms.CharField(max_length=20, required=False)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    @transaction.atomic
    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data.get("first_name", ""),
            last_name=self.cleaned_data.get("last_name", ""),
            email=self.cleaned_data.get("email", ""),
            phone=self.cleaned_data.get("phone", ""),
            role=User.Role.MEMBER,
        )
        user.set_password(self.cleaned_data["password1"])
        user.save()

        member = Member(
            user=user,
            skill_level=self.cleaned_data["skill_level"],
            date_of_birth=self.cleaned_data.get("date_of_birth"),
            emergency_contact_name=self.cleaned_data.get("emergency_contact_name", ""),
            emergency_contact_phone=self.cleaned_data.get("emergency_contact_phone", ""),
            notes=self.cleaned_data.get("notes", ""),
        )
        member.save()
        return member


class MemberUpdateForm(forms.ModelForm):
    """updates the member profile fields only."""

    class Meta:
        model = Member
        fields = [
            "skill_level",
            "date_of_birth",
            "emergency_contact_name",
            "emergency_contact_phone",
            "notes",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class UserInlineForm(forms.ModelForm):
    """inline form for editing the linked user's basic info on the member update page."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]
