from django.db import models
from django.utils.text import slugify
from users.models import User

from .tasks import generate_short_id


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("open", "Open"),
        ("on_hold", "On Hold"),
        ("resolved", "Resolved"),
    )
    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    )
    ref = models.CharField(
        max_length=8, unique=True, default=generate_short_id, editable=False, null=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="low")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="tickets_created",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="tickets_updated_by",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    attachment = models.FileField(
        upload_to="ticket_attachments/", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ref)
        super(Ticket, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TicketAssignment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="assigned_tickets")
    assign_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="+"
    )
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ticket {self.ticket.title} assigned to {self.assigned_to.username}"


class TicketSolution(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="solutions"
    )
    cause = models.TextField()
    solution = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Solution for {self.ticket.title}"


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket, related_name="comments", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, related_name="ticket_comments", on_delete=models.CASCADE
    )
    comment = models.TextField()
    # the_fix = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.ticket.title}"
