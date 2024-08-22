from django import forms

from .models import User


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "profile_picture",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]


class ManagerUserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "profile_picture",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
        ]

    def __init__(self, *args, **kwargs):
        super(ManagerUserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["role"].initial = self.instance.roles.all()
