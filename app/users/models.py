from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("agent", "Support Agent"),
        ("admin", "Admin"),
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")
    profile_picture = models.FileField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
