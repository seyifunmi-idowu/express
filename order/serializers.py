from rest_framework import serializers

from order.models import Vehicle


class RetrieveVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "name", "note", "file_url")
