from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserProfileForm(forms.ModelForm):
    """reusable user fields used as a base for member and trainer registration."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone"]

    def clean_password1(self):
        pw = self.cleaned_data.get("password1")
        if pw:
            validate_password(pw)
        return pw

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("password1")
        pw2 = cleaned.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned
