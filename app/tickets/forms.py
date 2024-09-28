from django import forms
from users.models import User

from .models import Category, Comment, Ticket, TicketAssignment, TicketSolution


class TicketAssignmentForm(forms.ModelForm):
    class Meta:
        model = TicketAssignment
        fields = ["assign_to"]
        widgets = {
            "assign_to": forms.Select(attrs={"onchange": "this.form.submit();"}),
        }
        
    def __init__(self, *args, **kwargs):
        super(TicketAssignmentForm, self).__init__(*args, **kwargs)
        # Filter the queryset for 'assign_to' field to include only 'Support Agent' users
        self.fields["assign_to"].queryset = User.objects.filter(role="agent")


class TicketSolutionForm(forms.ModelForm):
    class Meta:
        model = TicketSolution
        fields = ["cause", "solution"]
        widgets = {
            "cause": forms.Textarea(
                attrs={
                    "rows": 4,  # Set the number of rows to display
                    "placeholder": "Enter ticket cause here...",  # Optional: Add a placeholder
                }
            ),
            "solution": forms.Textarea(
                attrs={
                    "rows": 4,  # Set the number of rows to display
                    "placeholder": "Enter ticket fix here...",  # Optional: Add a placeholder
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
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
            "status",
            "priority",
            "category",
        ]

        widgets = {
            # "cause": forms.Textarea(
            #     attrs={
            #         "rows": 4,  # Set the number of rows to display
            #         "placeholder": "Enter ticket cause here...",  # Optional: Add a placeholder
            #     }
            # ),
            # "resolution": forms.Textarea(
            #     attrs={
            #         "rows": 4,  # Set the number of rows to display
            #         "placeholder": "Enter ticket fix here...",  # Optional: Add a placeholder
            #     }
            # ),
            "priority": forms.Select(attrs={"onchange": "this.form.submit()"}),
            "status": forms.Select(attrs={"onchange": "this.form.submit()"}),
            "category": forms.Select(attrs={"onchange": "this.form.submit()"}),
        }

   
    
