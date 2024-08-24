from django import forms
from users.models import User

from .models import Category, Comment, Ticket


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "the_fix"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add a comment..."}
            ),
        }


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
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
        super(TicketForm, self).__init__(*args, **kwargs)
        # Filter the queryset for 'assigned_to' field to include only 'Support Agent' users
        self.fields["assigned_to"].queryset = User.objects.filter(role="agent")


class TicketAssignForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "assigned_to",
        ]

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        # Filter the queryset for 'assigned_to' field to include only 'Support Agent' users
        self.fields["assigned_to"].queryset = User.objects.filter(role="agent")
