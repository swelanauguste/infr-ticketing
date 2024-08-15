from django.urls import path

from . import views

urlpatterns = [
    path("detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("update/<int:pk>/", views.update_user, name="user_update"),
]
