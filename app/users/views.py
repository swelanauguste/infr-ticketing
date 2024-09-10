import after_response
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, UpdateView
from users.models import User

from .forms import UserUpdateForm, UserCustomCreationForm
from .models import User
from .tasks import user_registration_email
from .tokens import account_activation_token


class UserLoginView(auth_views.LoginView):
    template_name = "users/login.html"


def logout_view(request):
    logout(request)
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return redirect("login")


def user_registration_view(request):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_registration_email.after_response(
                request, user, form.cleaned_data["email"]
            )
            # user_registration_email(request, user, form.cleaned_data.get("email"))
            return redirect("login")
    else:
        form = UserCustomCreationForm()
    return render(request, "users/register.html", {"form": form})


# @login_required
# def ticket_detail(request, pk):
#     ticket = get_object_or_404(Ticket, pk=pk)
#     comments = ticket.comments.all().order_by("-created_at")
#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.ticket = ticket
#             comment.author = request.user
#             comment.save()
#             messages.success(request, "Comment added successfully.")
#             return redirect("user-ticket-detail", pk=ticket.pk)
#     else:
#         comment_form = CommentForm()
#     context = {
#         "ticket": ticket,
#         "comments": comments,
#         "comment_form": comment_form,
#     }
#     return render(request, "users/tickets/detail.html", context)


# @login_required
# def user_ticket_list(request):
#     tickets = (
#         Ticket.objects.filter(created_by=request.user)
#         .exclude(status="closed")
#         .order_by("-created_at")[:10]
#     )
#     return render(request, "users/tickets/list.html", {"tickets": tickets})


@login_required
def user_update(request):
    user = get_object_or_404(User, pk=request.user.pk)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(
                "user-detail",
            )  # Redirect to a user detail or other page
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/user_form.html", {"form": form, "user": user})


@login_required
def user_detail(request):
    if request.user.role == "admin" or request.user.role == "agent":
        user = get_object_or_404(User, pk=request.user.id)
    else:
        user = get_object_or_404(User, pk=request.user.id)
    return render(request, "users/user_detail.html", {"user": user})
    return render(request, "users/user_detail.html", {"user": user})
