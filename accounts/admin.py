from django.contrib import admin
from .models import Account
from django.utils.html import format_html


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_display")

    def icon_display(self, obj):
        return (
            format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
            if obj.icon
            else "No Image"
        )

    icon_display.short_description = "Icon"
