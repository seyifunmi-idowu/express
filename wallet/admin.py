from django.contrib import admin

from wallet.models import BankAccount, Card, Transaction, Wallet

# Register your models here.


class WalletAdmin(admin.ModelAdmin):
    search_fields = ("user__first_name", "user__last_name")
    readonly_fields = ("user", "balance")
    list_display = ("user", "balance")
    ordering = ("user__first_name", "user__last_name")
    exclude = ("state", "created_by", "deleted_by", "updated_by", "deleted_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction)
admin.site.register(Card)
admin.site.register(BankAccount)
