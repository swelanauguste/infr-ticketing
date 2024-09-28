from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_ticket_list, name="ticket-list-user"),
    path(
        "assigned/ticket-list/", views.ticket_list_assigned, name="ticket-list-assigned"
    ),
    path("ticket-list/", views.ticket_list, name="ticket-list"),
    path("create/", views.ticket_create, name="ticket-create"),
    path(
        "detail/<slug:slug>/",
        views.ticket_detail,
        name="ticket-detail",
    ),
    path(
        "ticket/assign/<slug:slug>/",
        views.ticket_assign_view,
        name="ticket-assign",
    ),
]
