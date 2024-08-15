from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_ticket_list, name="user_ticket_list"),
    path("support/ticket_list/", views.support_ticket_list, name="support_ticket_list"),
    path("create/", views.create_ticket, name="create_ticket"),
    path("detail/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("support/detail/<int:pk>/", views.ticket_support_detail, name="ticket_support_detail"),
]
