from django.contrib import admin

from .models import ActionItem


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ["id", "description_preview", "completed", "created_at"]
    list_filter = ["completed", "created_at"]
    search_fields = ["description"]
    readonly_fields = ["id", "created_at"]
    list_editable = ["completed"]

    fieldsets = (
        (None, {"fields": ("id", "description", "completed")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def description_preview(self, obj):
        """Show a preview of the description."""
        if len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description

    description_preview.short_description = "Description"
