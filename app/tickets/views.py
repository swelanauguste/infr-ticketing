from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from users.models import User

from .forms import CommentForm, TicketCreateForm, TicketUpdateForm
from .models import Ticket
from .tasks import ticket_add_comment_email, ticket_assigned_email, ticket_created_email


@login_required
def ticket_list_assigned(request):
    tickets = Ticket.objects.filter(assigned_to=request.user)
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_support_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    # if ticket.created_by != request.user and ticket.assigned_to != request.user:
    #     return redirect("ticket-list")

    if request.method == "POST":
        form = TicketUpdateForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.updated_by = request.user
            ticket.save()
            messages.success(request, "Ticket has been updated successfully!")
            return redirect(
                "ticket-support-detail", pk=ticket.pk
            )  # Redirect to the ticket detail page
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(
        request, "tickets/ticket_detail_support.html", {"form": form, "ticket": ticket}
    )


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(
                commit=False
            )  # Create the ticket instance but don't save it yet
            ticket.created_by = request.user  # Set 'created_by' to the logged-in user
            ticket.save()  # Save the ticket to the database
            messages.success(request, "Ticket has been created successfully!")
            ticket_created_email.after_response(ticket)
            return redirect(
                "ticket-list-user"
            )  # Redirect to the ticket list or another relevant page
    else:
        form = TicketCreateForm()

    return render(request, "tickets/create_ticket.html", {"form": form})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.all().order_by("-created_at")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect("ticket-detail-user", pk=ticket.pk)
    else:
        comment_form = CommentForm()
    context = {
        "ticket": ticket,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "tickets/users/detail.html", context)


@login_required
def user_ticket_list(request):
    tickets = (
        Ticket.objects.filter(created_by=request.user)
        .exclude(status="closed")
        .order_by("-created_at")[:10]
    )
    return render(request, "tickets/users/list.html", {"tickets": tickets})
