from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]


class UserCustomCreationForm(UserCreationForm):
    allowed_domains = ["goslnet.gov.lc", "govt.lc"]

    usable_password = None

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]

        # Validate email domain
        if domain not in self.allowed_domains:
            raise forms.ValidationError(
                f"Email address must end with one of the allowed domains: {', '.join(self.allowed_domains)}"
            )
        return email

    def clean_username(self):
        # cleaned_data = super().clean()
        email = cleaned_data.get("email")

        # Ensure the username derived from email is unique
        if email:
            username = email.split("@")[0]
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    f"The username '{username}' is already taken. Please use a different email."
                )

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].split("@")[
            0
        ]  # Set username based on email
        user.is_active = False  # Set user as inactive by default
        if commit:
            user.save()
        return user
