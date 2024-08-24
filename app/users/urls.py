from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_detail, name="user-detail"),
    path("user/update/<int:pk>/", views.update_user, name="user-update"),
    path("user-ticket-list/", views.user_ticket_list, name="user-ticket-list"),
    path("user-ticket-detail/<int:pk>/", views.ticket_detail, name="user-ticket-detail"),
]
