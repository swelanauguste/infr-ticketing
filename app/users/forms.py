from django import forms

from .models import Role, User


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
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = User
        fields = [
            "profile_picture",
            "first_name",
            "last_name",
            "email",
            "phone",
            "roles",
        ]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["roles"].initial = self.instance.roles.all()
