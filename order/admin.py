from django.contrib import admin

from order.models import Vehicles


class VehiclesAdmin(admin.ModelAdmin):
    search_fields = ("name", "status")
    readonly_fields = ("created_by", "created_at")
    list_display = ("name", "status")
    ordering = ["name"]
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")


admin.site.register(Vehicles, VehiclesAdmin)
