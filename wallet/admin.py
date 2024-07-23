# from django.contrib import admin
#
# from wallet.models import Transaction, Wallet
#
# # Register your models here.
#
#
# class WalletAdmin(admin.ModelAdmin):
#     search_fields = ("user__first_name", "user__last_name")
#     readonly_fields = ("user", "balance")
#     list_display = ("user", "balance")
#     ordering = ("user__first_name", "user__last_name")
#     exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")
#
#     def get_queryset(self, request):
#         return self.model.objects.exclude(user__state="DELETED")
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#
# class TransactionAdmin(admin.ModelAdmin):
#     search_fields = (
#         "user__first_name",
#         "user__last_name",
#         "transaction_type",
#         "transaction_status",
#         "amount",
#         "reference",
#     )
#     list_display = (
#         "user",
#         "amount",
#         "reference",
#         "transaction_type",
#         "transaction_status",
#         "payment_category",
#         "created_at",
#     )
#     ordering = ["-created_at"]
#     exclude = (
#         "state",
#         "created_by",
#         "deleted_by",
#         "updated_by",
#         "deleted_at",
#         "wallet_id",
#         "object_id",
#         "object_class",
#     )
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def get_queryset(self, request):
#         return self.model.objects.exclude(user__state="DELETED")
#
#
# admin.site.register(Wallet, WalletAdmin)
# admin.site.register(Transaction, TransactionAdmin)
