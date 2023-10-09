from django.contrib import admin
from django.utils.html import format_html

from rider.models import Rider, RiderDocument

# Register your models here.


class RiderDocumentInline(admin.TabularInline):
    model = RiderDocument
    readonly_fields = ("type", "file_url_link", "number")
    ordering = ("type",)
    fields = ("file_url_link", "type", "number", "verified")
    extra = 0

    def file_url_link(self, instance):
        if instance.file_url:
            return format_html(
                '<a href="{}" target="_blank" download="">{}</a>',
                instance.file_url,
                instance.file_url,
            )
        else:
            return ""

    file_url_link.short_description = "File URL"  # type: ignore

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield


class RiderAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "vehicle_plate_number",
        "vehicle_make",
        "vehicle_model",
    )
    readonly_fields = (
        "user",
        "avatar_url",
        "vehicle_plate_number",
        "vehicle_color",
        "vehicle_type",
        "vehicle_make",
        "vehicle_model",
        "city",
    )
    list_display = ("get_name", "status")
    ordering = ("-created_at",)
    exclude = (
        "status_updates",
        "operation_locations",
        "state",
        "created_by",
        "deleted_by",
        "updated_by",
        "deleted_at",
    )
    inlines = [RiderDocumentInline]

    def get_name(self, obj):
        return obj.display_name


admin.site.register(Rider, RiderAdmin)
