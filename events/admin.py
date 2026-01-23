# events/admin.py
from django.contrib import admin
from .models import Event, EventImage, EmailNotificationConfig

@admin.register(EmailNotificationConfig)
class EmailNotificationConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if EmailNotificationConfig.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
