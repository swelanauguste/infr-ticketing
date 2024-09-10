import after_response
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags


@after_response.enable
def ticket_created_email(ticket):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"{ticket.title}"
    ticket_url = reverse("user-ticket-detail", kwargs={"pk": ticket.pk})
    full_url = f"http://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/emails/ticket_create.html", {"ticket": ticket, "full_url": full_url}
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,  # subject of email
        plain_message,  # body of email
        settings.DEFAULT_FROM_EMAIL,  # from email
        [
            ticket.created_by.email,
            settings.DEFAULT_FROM_EMAIL,
        ],  # to emails
        html_message=html_message,
    )

@after_response.enable
def ticket_assigned_email(ticket):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"{ticket.title}"
    ticket_url = reverse("user-ticket-detail", kwargs={"pk": ticket.pk})
    full_url = f"http://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/emails/ticket_create.html", {"ticket": ticket, "full_url": full_url}
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,  # subject of email
        plain_message,  # body of email
        settings.DEFAULT_FROM_EMAIL,  # from email
        [
            ticket.created_by.email,
            settings.DEFAULT_FROM_EMAIL,
        ],  # to emails
        html_message=html_message,
    )


@after_response.enable
def ticket_add_comment_email(ticket):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"{ticket.title}"
    ticket_url = reverse("user-ticket-detail", kwargs={"pk": ticket.pk})
    full_url = f"http://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/emails/ticket_add_comment.html", {"ticket": ticket, "full_url": full_url}
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,  # subject of email
        plain_message,  # body of email
        settings.DEFAULT_FROM_EMAIL,  # from email
        [
            ticket.created_by.email,
            settings.DEFAULT_FROM_EMAIL,
        ],  # to emails
        html_message=html_message,
    )
