from django.contrib import admin
from users.models import User

from .models import Category, Tag, Ticket

admin.site.register(Tag)
admin.site.register(Category)


class TicketAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(role="agent")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Ticket, TicketAdmin)
