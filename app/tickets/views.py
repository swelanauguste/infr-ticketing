from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from users.models import User

from .forms import TicketCreateForm, TicketUpdateForm, TicketAssignForm, CommentForm
from .models import Ticket
from .tasks import ticket_assigned_email, ticket_created_email


@login_required
def support_ticket_list(request):
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
            messages.success(request, "Ticket has been updated successfully!")
            return redirect(
                "ticket-support-detail", pk=ticket.pk
            )  # Redirect to the ticket detail page
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(
        request, "tickets/update_ticket.html", {"form": form, "ticket": ticket}
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
                "user-ticket-list"
            )  # Redirect to the ticket list or another relevant page
    else:
        form = TicketCreateForm()

    return render(request, "tickets/create_ticket.html", {"form": form})


@login_required
def ticket_assigned(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = TicketAssignForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(
                commit=False
            )  # Create the ticket instance but don't save it yet
            ticket.updated_by = request.user  # Set 'created_by' to the logged-in user
            ticket.assigned_by = request.user  # Set 'assigned_by' to the logged-in user
            ticket.save()  # Save the ticket to the database
            messages.success(
                request,
                f"Ticket has been assigned to {ticket.assigned_to}!",
            )
            ticket_assigned_email.after_response(ticket)
            return redirect(
                "ticket-support-detail", pk=ticket.pk
            )  # Redirect to the ticket detail page
    else:
        form = TicketAssignForm()

    return render(request, "tickets/create_ticket.html", {"form": form})
