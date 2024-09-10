from django.contrib import admin
from users.models import User

from .models import Category, Comment, Ticket

admin.site.register(Category)
admin.site.register(Comment)


class TicketAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(role="agent")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = [
        "title",
        "category",
        "created_at",
        "created_by",
        "assigned_to",
    ]
    list_editable = ["category", "assigned_to"]
    list_filter = ["category", "created_by", "assigned_to"]


admin.site.register(Ticket, TicketAdmin)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ["username", "role"]
#     list_editable =  ["role"]


# admin.site.register(User, UserAdmin)
