from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_ticket_list, name="ticket-list-user"),
    path("detail/<int:pk>/", views.ticket_detail, name="ticket-detail-user"),
    path("support/ticket_list/", views.ticket_list_assigned, name="ticket-list-assigned"),
    path("ticket_list/", views.ticket_list, name="ticket-list"),
    path("create/", views.ticket_create, name="ticket-create"),

    path(
        "support/detail/<int:pk>/",
        views.ticket_support_detail,
        name="ticket-support-detail",
    ),
]
