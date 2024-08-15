from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from users.models import User

from .forms import TicketCreateForm, TicketUpdateForm
from .models import Ticket


@login_required
def user_ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by("-created_at")[:10]
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})

@login_required
def support_ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@login_required
def ticket_support_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.created_by != request.user and ticket.assigned_to != request.user:
        return redirect("ticket_list")

    if request.method == "POST":
        form = TicketUpdateForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()  # Save the updated ticket
            messages.success(request, 'Ticket has been updated successfully!')
            return redirect(
                "ticket_support_detail", pk=ticket.pk
            )  # Redirect to the ticket detail page
    else:
        form = TicketUpdateForm(instance=ticket)

    return render(
        request, "tickets/update_ticket.html", {"form": form, "ticket": ticket}
    )

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(
                commit=False
            )  # Create the ticket instance but don't save it yet
            ticket.created_by = request.user  # Set 'created_by' to the logged-in user
            ticket.save()  # Save the ticket to the database
            messages.success(request, 'Ticket has been created successfully!')
            return redirect(
                "user_ticket_list"
            )  # Redirect to the ticket list or another relevant page
    else:
        form = TicketCreateForm()

    return render(request, "tickets/create_ticket.html", {"form": form})
