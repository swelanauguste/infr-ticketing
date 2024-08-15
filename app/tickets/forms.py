from django import forms
from users.models import User, Role

from .models import Category, Ticket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
            "category",
            "attachment",
            "tags",
        ]

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,  # Set the number of rows to display
                "placeholder": "Enter ticket description here...",  # Optional: Add a placeholder
            }
        )
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(TicketCreateForm, self).__init__(*args, **kwargs)
        # Optionally, you can customize the queryset for categories as well
        self.fields["category"].queryset = Category.objects.all()


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
            "assigned_to",
            "category",
            "attachment",
        ]

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,  # Set the number of rows to display
                "placeholder": "Enter ticket description here...",  # Optional: Add a placeholder
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TicketUpdateForm, self).__init__(*args, **kwargs)
        # Filter users with 'tech' role for the 'assigned_to' field
        tech_role = Role.objects.get(name='tech')
        self.fields['assigned_to'].queryset = User.objects.filter(roles=tech_role)
        # Optionally, you can customize the queryset for categories as well
        self.fields["category"].queryset = Category.objects.all()
