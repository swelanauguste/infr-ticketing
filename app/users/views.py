from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, UpdateView

from .forms import UserUpdateForm
from .models import Role, User


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
                "user_detail", pk=user.id
            )  # Redirect to a user detail or other page
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/user_form.html", {"form": form, "user": user})


class UserDetailView(DetailView):
    model = User

