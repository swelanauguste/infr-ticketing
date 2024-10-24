import threading

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from users.models import User

from .forms import (
    CommentForm,
    TicketAssignmentForm,
    TicketCreateForm,
    TicketSolutionForm,
    TicketUpdateForm,
)
from .models import Ticket, TicketAssignment
from .tasks import (
    ticket_add_comment_email,
    ticket_assigned_email,
    ticket_created_email,
    ticket_resolved_email,
)


@login_required
def ticket_list_assigned(request):
    status_filter = request.GET.get("status", "")
    # Get the latest assignment for each ticket
    latest_assignment = TicketAssignment.objects.filter(ticket=OuterRef("pk")).order_by(
        "-created_at"
    )
    assigned_tickets = Ticket.objects.filter(
        assigned_tickets__in=Subquery(
            latest_assignment.values("pk")[
                :1
            ]  # Get only the most recent assignment per ticket
        ),
        assigned_tickets__assign_to=request.user,  # Assigned to the logged-in user
    ).distinct()
    # if status_filter == "all":
    #     # Get tickets assigned to the current user based on the most recent assignment
    #     assigned_tickets = Ticket.objects.filter(
    #     assigned_tickets__in=Subquery(
    #         latest_assignment.values("pk")[
    #             :1
    #         ]  # Get only the most recent assignment per ticket
    #     ),
    #     assigned_tickets__assign_to=request.user,  # Assigned to the logged-in user
    # ).distinct()
    if status_filter:
        assigned_tickets = assigned_tickets.filter(status=status_filter)
    else:
        assigned_tickets = assigned_tickets.exclude(
            status="resolved"
        )  # Default: show unresolved tickets
    return render(request, "tickets/ticket_list.html", {"tickets": assigned_tickets, 'status_filter': status_filter})


@login_required
def ticket_list(request):
    status_filter = request.GET.get("status", "")

    if status_filter == "all":
        tickets = Ticket.objects.all()  # Return all tickets if 'all' is selected
    elif status_filter:
        tickets = Ticket.objects.filter(
            status=status_filter
        )  # Filter tickets based on selected status
    else:
        tickets = Ticket.objects.exclude(
            status="resolved"
        )  # Default: show unresolved tickets

    return render(
        request,
        "tickets/ticket_list.html",
        {"tickets": tickets, "status_filter": status_filter},
    )


@login_required
def user_ticket_list(request):
    status_filter = request.GET.get("status", "")

    if status_filter == "all":
        tickets = (
            Ticket.objects.filter(created_by=request.user)
            .exclude(status="resolved")
            .order_by("-created_at")[:10]
        )
    elif status_filter:
        tickets = Ticket.objects.filter(created_by=request.user).filter(status=status_filter)
    else:
        tickets = (
            Ticket.objects.filter(created_by=request.user)
            .exclude(status="resolved")
            .order_by("-created_at")[:10]
        )
    return render(
        request,
        "tickets/users/list.html",
        {"tickets": tickets, "status_filter": status_filter},
    )


@login_required
def ticket_assign_view(request, slug):
    # Get the specific complaint
    ticket = get_object_or_404(Ticket, slug=slug)

    if request.method == "POST":
        form = TicketAssignmentForm(request.POST)
        if form.is_valid():
            assign_to = form.cleaned_data["assign_to"]
            assign = form.save(commit=False)
            assign.ticket = ticket
            assign.created_by = request.user
            assign.save()
            messages.success(
                request,
                "Ticket has been assigned to {} successfully!".format(assign_to),
            )
            # ticket_assigned_email.after_response(ticket)
            assign_email_thread = threading.Thread(
                target=ticket_assigned_email, args=(ticket,)
            )
            assign_email_thread.start()

            # Redirect back to the complaint detail page or the page you want
            return redirect(reverse_lazy("ticket-detail", kwargs={"slug": slug}))

    # No need to handle the 'GET' request or render a template,
    # since the form is being posted and handled via another page.
    return redirect(reverse_lazy("ticket-detail", kwargs={"slug": slug}))


@login_required
def ticket_detail(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    old_status = ticket.status  # Store the old status before saving the form

    if request.method == "POST":
        form = TicketUpdateForm(request.POST, request.FILES, instance=ticket)
        comment_form = CommentForm(request.POST)
        solution_form = TicketSolutionForm(request.POST)
        if (
            request.POST and form.is_valid()
        ):  # Check if the ticket update form was submitted
            ticket = form.save(commit=False)
            ticket.updated_by = request.user  # Log the user who updated the ticket
            ticket.save()
            # Check if the status was changed to 'resolved'
            if old_status != ticket.status and ticket.status == "resolved":
                # Send email notification if status is changed to resolved
                # send_email_on_ticket_closed(ticket)
                messages.success(request, "Ticket has been closed")
            messages.success(request, "Ticket has been updated successfully!")
            return redirect("ticket-detail", slug=ticket.slug)

        if (
            request.POST and comment_form.is_valid()
        ):  # Check if the comment form was submitted
            comment = comment_form.save(commit=False)
            comment.ticket = ticket  # Link the comment to the ticket
            comment.created_by = request.user  # Set the created_by of the comment
            comment.save()
            messages.success(request, "Comment has been added successfully!")
            # ticket_add_comment_email.after_response(ticket, comment)
            add_comment_email_thread = threading.Thread(
                target=ticket_add_comment_email, args=(ticket, comment)
            )
            add_comment_email_thread.start()
            return redirect("ticket-detail", slug=ticket.slug)
        if (
            request.POST and solution_form.is_valid()
        ):  # Check if the comment form was submitted
            solution = solution_form.save(commit=False)
            solution.ticket = ticket  # Link the solution to the ticket
            solution.created_by = request.user  # Set the created_by of the solution
            solution.save()
            # ticket_resolved_email.after_response(ticket, solution)
            ticket_resolved_email_thread = threading.Thread(
                target=ticket_resolved_email, args=(ticket, solution)
            )
            ticket_resolved_email_thread.start()
            messages.success(request, "Solution has been added successfully!")
            return redirect("ticket-detail", slug=ticket.slug)

    else:
        form = TicketUpdateForm(instance=ticket)
        comment_form = CommentForm(initial={"ticket": ticket})
        solution_form = TicketSolutionForm(initial={"ticket": ticket})
        try:
            ticket_assign_form = TicketAssignmentForm(
                initial={"assign_to": ticket.assigned_tickets.first().assign_to}
            )
        except:
            ticket_assign_form = TicketAssignmentForm()

    return render(
        request,
        "tickets/ticket_detail.html",
        {
            "form": form,
            "ticket": ticket,
            "comment_form": comment_form,
            "solution_form": solution_form,
            "ticket_assign_form": ticket_assign_form,
        },
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
            # ticket_created_email.after_response(ticket)
            ticket_created_email_thread = threading.Thread(
                target=ticket_created_email, args=(ticket,)
            )
            ticket_created_email_thread.start()
            return redirect(
                "ticket-list-user"
            )  # Redirect to the ticket list or another relevant page
    else:
        form = TicketCreateForm()

    return render(request, "tickets/create_ticket.html", {"form": form})
