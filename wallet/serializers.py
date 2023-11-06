from rest_framework import serializers

from wallet.models import Card


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


class ChargeCardSerializer(serializers.Serializer):
    card_id = serializers.CharField(max_length=50)
    amount = serializers.FloatField()
