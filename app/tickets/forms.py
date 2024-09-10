from django import forms
from users.models import User

from .models import Category, Comment, Ticket


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
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
            "priority",
            "category",
            "assigned_to",
            "cause",
            "fix",
        ]

        widgets = {
            "cause": forms.Textarea(
                attrs={
                    "rows": 4,  # Set the number of rows to display
                    "placeholder": "Enter ticket cause here...",  # Optional: Add a placeholder
                }
            ),
            "fix": forms.Textarea(
                attrs={
                    "rows": 4,  # Set the number of rows to display
                    "placeholder": "Enter ticket fix here...",  # Optional: Add a placeholder
                }
            ),
            "priority": forms.Select(attrs={"onchange": "this.form.submit()"}),
            "assigned_to": forms.Select(attrs={"onchange": "this.form.submit()"}),
            "category": forms.Select(attrs={"onchange": "this.form.submit()"}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketUpdateForm, self).__init__(*args, **kwargs)
        # Filter the queryset for 'assigned_to' field to include only 'Support Agent' users
        self.fields["assigned_to"].queryset = User.objects.filter(role="agent")
