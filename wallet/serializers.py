from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from wallet.models import BankAccount, Card, Transaction


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "card_type",
            "last_4",
            "exp_month",
            "exp_year",
            "country_code",
            "brand",
        ]


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["id", "account_number", "account_name", "bank_name"]


class GetTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_type",
            "transaction_status",
            "amount",
            "currency",
            "reference",
            "description",
            "created_at",
        ]


class AddCardSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ChargeCardSerializer(serializers.Serializer):
    card_id = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class VerifyAccountNumberSerializer(serializers.Serializer):
    bank_code = serializers.CharField(max_length=50)
    account_number = serializers.CharField()

    def validate_account_number(self, account_number: str) -> str:
        if len(account_number) != 10:
            raise ValidationError("Account number must be 10 digits long.")
        return account_number


class TrasferFromWalletToBankSerializer(serializers.Serializer):
    bank_code = serializers.CharField(max_length=50)
    account_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    save_account = serializers.BooleanField(default=False, required=False)

    def validate_account_number(self, account_number: str) -> str:
        if len(account_number) != 10:
            raise ValidationError("Account number must be 10 digits long.")
        return account_number


class TrasferFromWalletToBeneficiarySerializer(serializers.Serializer):
    beneficiary_id = serializers.CharField(max_length=50)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
