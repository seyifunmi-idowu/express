from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    actions = ["hard_deleted_selected", "soft_deleted_selected"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def hard_deleted_selected(self, request, queryset):
        for record in queryset:
            record.hard_delete()

    hard_deleted_selected.short_description = "Hard Delete Selected"  # type: ignore

    def soft_deleted_selected(self, request, queryset):
        records_to_delete = queryset.filter(state="ACTIVE")
        for record in records_to_delete:
            record.delete()

    soft_deleted_selected.short_description = "Soft Delete Selected"  # type: ignore

    def delete_model(self, request, obj):
        obj.delete()
