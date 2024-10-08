# from django.contrib import admin
#
# from customer.models import BusinessCustomer, Customer, IndividualCustomer
#
#
# class CustomerAdmin(admin.ModelAdmin):
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
#     )
#     list_display = ("user", "customer_type", "business_name")
#     ordering = ("user__first_name", "user__last_name")
#     exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")
#
#     def has_add_permission(self, request, obj=None):
#         return False
#
#     def get_queryset(self, request):
#         return self.model.objects.exclude(user__state="DELETED")
#
#
# class IndividualCustomerAdmin(admin.ModelAdmin):
#     search_fields = ("user__first_name", "user__last_name")
#     readonly_fields = ("user", "customer_type")
#     list_display = ("user", "customer_type", "business_name")
#     ordering = ("user__first_name", "user__last_name")
#     exclude = (
#         "business_name",
#         "business_address",
#         "business_category",
#         "delivery_volume",
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
#         return self.model.objects.filter(customer_type="INDIVIDUAL").exclude(
#             user__state="DELETED"
#         )
#
#
# class BusinessCustomerAdmin(CustomerAdmin):
#     def get_queryset(self, request):
#         return self.model.objects.filter(customer_type="BUSINESS").exclude(
#             user__state="DELETED"
#         )
#
#
# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(IndividualCustomer, IndividualCustomerAdmin)
# admin.site.register(BusinessCustomer, BusinessCustomerAdmin)


from django.contrib import admin
from unfold.admin import ModelAdmin

from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):  # Use UnfoldAdmin instead of ModelAdmin
    search_fields = (
        "user__first_name",
        "user__last_name",
        "business_name",
        "business_category",
    )
    readonly_fields = (
        "user",
        "business_address",
        "business_category",
        "delivery_volume",
    )
    list_display = ("user", "customer_type", "business_name")
    ordering = ("user__first_name", "user__last_name")
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")
    list_filter = ("customer_type",)  # Add customer_type to list_filter

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return self.model.objects.exclude(user__state="DELETED")
