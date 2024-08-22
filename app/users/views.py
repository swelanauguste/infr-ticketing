from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, UpdateView
from tickets.forms import CommentForm
from tickets.models import Comment, Ticket

from .forms import UserUpdateForm
from .models import User


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
            return redirect("user-ticket-detail", pk=ticket.pk)
    else:
        comment_form = CommentForm()
    context = {
        "ticket": ticket,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "users/tickets/detail.html", context)


@login_required
def user_ticket_list(request):
    tickets = (
        Ticket.objects.filter(created_by=request.user)
        .exclude(status="closed")
        .order_by("-created_at")[:10]
    )
    return render(request, "users/tickets/list.html", {"tickets": tickets})


@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()  # Save many-to-many data for the form.
            return redirect(
                "user-detail", pk=user.id
            )  # Redirect to a user detail or other page
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/user_form.html", {"form": form, "user": user})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


@login_required
def user_detail(request):
    if request.user.role == "admin" or request.user.role == "agent":
        user = get_object_or_404(User, pk=request.user.id)
    else:
        user = get_object_or_404(User, pk=request.user.id)
    return render(request, "users/user_detail.html", {"user": user})
