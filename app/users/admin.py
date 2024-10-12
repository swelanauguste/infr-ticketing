from django.contrib import admin

from .models import Department, User


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "role"]
    list_editable = ["role"]


admin.site.register(User, UserAdmin)
admin.site.register(Department)
