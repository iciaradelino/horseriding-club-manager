from django import forms
from .models import Horse, HealthRecord


class HorseForm(forms.ModelForm):
    class Meta:
        model = Horse
        fields = ["name", "breed", "date_of_birth", "color", "status", "notes", "photo"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ["record_type", "date", "description", "performed_by", "next_due_date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "next_due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
