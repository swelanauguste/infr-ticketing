from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user-detail/", views.user_detail, name="user-detail"),
    path("user-update/", views.user_update, name="user-update"),
    path("register/", views.user_registration_view, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
