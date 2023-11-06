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
