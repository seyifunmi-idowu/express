# from django.contrib import admin
#
# from business.models import Business
#
#
# class BusinessAdmin(admin.ModelAdmin):
#     search_fields = (
#         "user__first_name",
#         "user__last_name",
#         "business_name",
#         "business_category",
#     )
#     readonly_fields = (
#         "user",
#         "business_address",
#         "business_category",
#         "delivery_volume",
#         "webhook_url",
#     )
#     list_display = ("user", "business_name", "business_type")
#     ordering = ("business_name",)
#     exclude = (
#         "e_secret_key",
#         "state",
#         "created_by",
#         "deleted_by",
#         "updated_by",
#         "deleted_at",
#     )
#
#     def has_add_permission(self, request, obj=None):
#         return False
#
#     def get_queryset(self, request):
#         return self.model.objects.exclude(user__state="DELETED")
#
#
# admin.site.register(Business, BusinessAdmin)
