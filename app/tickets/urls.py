from django.urls import path

from . import views

urlpatterns = [
    path("support/ticket_list/", views.support_ticket_list, name="support-ticket-list"),
    path("create/", views.ticket_create, name="ticket-create"),

    path("assign/<int:pk>/", views.ticket_assigned, name="ticket-assign"),
    path(
        "support/detail/<int:pk>/",
        views.ticket_support_detail,
        name="ticket-support-detail",
    ),
]
