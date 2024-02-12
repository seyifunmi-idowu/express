from rest_framework import serializers

from order.models import Order, Vehicle


class RetrieveVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "name", "note", "file_url")


class GetOrderSerializer(serializers.ModelSerializer):
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    # distance = serializers.SerializerMethodField()
    # duration = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    assigned_by_customer = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "status",
            "pickup",
            "delivery",
            "assigned_by_customer",
            "created_at",
        )

    def get_pickup(self, obj):
        return {"address": obj.pickup_location}

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_delivery(self, obj):
        return {"address": obj.delivery_location}

    def get_assigned_by_customer(self, obj):
        return obj.status == "PENDING_RIDER_CONFIRMATION"


class GetCurrentOrder(GetOrderSerializer):
    contact = serializers.SerializerMethodField()
    note_to_rider = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "status",
            "pickup",
            "delivery",
            "total_amount",
            "payment_method",
            "payment_by",
            "distance",
            "duration",
            "created_at",
            "contact",
            "note_to_rider",
        )

    def get_contact(self, obj):
        status = obj.status
        if status in [
            "PENDING",
            "PROCESSING_ORDER",
            "RIDER_ACCEPTED_ORDER",
            "RIDER_AT_PICK_UP",
        ]:
            destination = "pickup"
            contact = obj.pickup_number
        elif status in ["RIDER_PICKED_UP_ORDER", "ORDER_ARRIVED"]:
            destination = "delivery"
            contact = obj.delivery_number
        else:
            destination = None
            contact = ""

        return {"contact": contact, "destination": destination}

    def get_pickup(self, obj):
        split_address = obj.pickup_location.split(", ", 1)

        return {
            "address": obj.pickup_location,
            "longitude": obj.pickup_location_longitude,
            "latitude": obj.pickup_location_latitude,
            "short_address": split_address[0],
            "complete_address": split_address[1] if len(split_address) > 1 else "",
            "contact": obj.pickup_number,
            "contact_name": obj.pickup_contact_name,
            "time": obj.get_pick_up_time(),
        }

    def get_delivery(self, obj):
        split_address = obj.delivery_location.split(", ", 1)
        return {
            "address": obj.delivery_location,
            "longitude": obj.delivery_location_longitude,
            "latitude": obj.delivery_location_latitude,
            "short_address": split_address[0],
            "complete_address": split_address[1] if len(split_address) > 1 else "",
            "contact": obj.delivery_number,
            "contact_name": obj.delivery_contact_name,
            "time": obj.get_delivery_time(),
        }

    def get_distance(self, obj):
        from order.service import OrderService

        return OrderService.get_km_in_word(obj.distance)

    def get_duration(self, obj):
        from order.service import OrderService

        return OrderService.get_time_in_word(obj.duration)

    def get_note_to_rider(self, obj):
        return obj.order_meta_data.get("note_to_driver", "")


class CustomerOrderSerializer(serializers.ModelSerializer):
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    stopover = serializers.SerializerMethodField()
    note_to_driver = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "status",
            "payment_method",
            "payment_by",
            "pickup",
            "delivery",
            "stopover",
            "total_amount",
            "tip_amount",
            "note_to_driver",
            "distance",
            "duration",
            "timeline",
            "created_at",
        )

    def get_pickup(self, obj):
        return {
            "latitude": obj.pickup_location_latitude,
            "longitude": obj.pickup_location_longitude,
            "address": obj.pickup_location,
            "contact_name": obj.pickup_contact_name,
            "contact_phone_number": obj.pickup_number,
        }

    def get_delivery(self, obj):
        return {
            "latitude": obj.delivery_location_latitude,
            "longitude": obj.delivery_location_longitude,
            "address": obj.delivery_location,
            "contact_name": obj.delivery_contact_name,
            "contact_phone_number": obj.delivery_number,
        }

    def get_stopover(self, obj):
        stopover_list = [
            {
                "latitude": result.get("latitude"),
                "longitude": result.get("longitude"),
                "address": result.get("address"),
                "contact_name": result.get("contact_name"),
                "contact_phone_number": result.get("contact_number"),
            }
            for result in obj.order_stop_overs_meta_data
        ]
        return stopover_list

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_note_to_driver(self, obj):
        return obj.order_meta_data.get("note_to_driver")

    def get_timeline(self, obj):
        return obj.order_timeline

    def get_distance(self, obj):
        from order.service import OrderService

        return OrderService.get_km_in_word(obj.distance)

    def get_duration(self, obj):
        from order.service import OrderService

        return OrderService.get_time_in_word(obj.duration)


class RiderOrderSerializer(serializers.ModelSerializer):
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    stopover = serializers.SerializerMethodField()
    note_to_driver = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "status",
            "payment_method",
            "payment_by",
            "pickup",
            "delivery",
            "stopover",
            "total_amount",
            "tip_amount",
            "note_to_driver",
            "distance",
            "duration",
            "created_at",
        )

    def get_pickup(self, obj):
        return {
            "latitude": obj.pickup_location_latitude,
            "longitude": obj.pickup_location_longitude,
            "address": obj.pickup_location,
            "contact_name": obj.pickup_contact_name,
            "contact_phone_number": obj.pickup_number,
        }

    def get_delivery(self, obj):
        return {
            "latitude": obj.delivery_location_latitude,
            "longitude": obj.delivery_location_longitude,
            "address": obj.delivery_location,
            "contact_name": obj.delivery_contact_name,
            "contact_phone_number": obj.delivery_number,
        }

    def get_stopover(self, obj):
        stopover_list = [
            {
                "latitude": result.get("latitude"),
                "longitude": result.get("longitude"),
                "address": result.get("address"),
                "contact_name": result.get("contact_name"),
                "contact_phone_number": result.get("contact_number"),
            }
            for result in obj.order_stop_overs_meta_data
        ]
        return stopover_list

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_note_to_driver(self, obj):
        return obj.order_meta_data.get("note_to_driver")

    def get_distance(self, obj):
        from order.service import OrderService

        return OrderService.get_km_in_word(obj.distance)

    def get_duration(self, obj):
        from order.service import OrderService

        return OrderService.get_time_in_word(obj.duration)


class GetAddressInfoSerializer(serializers.Serializer):
    address = serializers.CharField(required=False)
    latitude = serializers.CharField(max_length=50)
    longitude = serializers.CharField(max_length=50)

    def validate(self, data):
        address = data.get("address")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not (
            address
            and not (latitude or longitude)
            or (latitude and longitude and not address)
        ):
            raise serializers.ValidationError(
                "Provide either 'address' or both 'latitude' and 'longitude', but not all three."
            )

        return data


class LocationSerializer(serializers.Serializer):
    latitude = serializers.CharField(max_length=50)
    longitude = serializers.CharField(max_length=50)
    address_details = serializers.CharField(max_length=200, required=False)
    contact_phone_number = serializers.CharField(max_length=50, required=False)
    contact_name = serializers.CharField(max_length=100, required=False)
    save_address = serializers.BooleanField(default=False)


class InitiateOrderSerializer(serializers.Serializer):
    pickup = LocationSerializer()
    delivery = LocationSerializer()
    stop_overs = LocationSerializer(many=True, required=False)
    vehicle_id = serializers.CharField(max_length=100, required=True)


class PlaceOrderSerializer(serializers.Serializer):
    PAYMENT_METHOD_CHOICES = [("WALLET", "WALLET"), ("CASH", "CASH")]
    PAYMENT_BY_CHOICES = [("SENDER", "SENDER"), ("RECIPIENT", "RECIPIENT")]

    note_to_driver = serializers.CharField(max_length=500, required=False)
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    payment_by = serializers.ChoiceField(choices=PAYMENT_BY_CHOICES, default="SENDER")
    favorite_rider = serializers.BooleanField(default=False)
    promo_code = serializers.CharField(max_length=20, required=False)


class AddDriverTipSerializer(serializers.Serializer):
    tip_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class AssignRiderSerializer(serializers.Serializer):
    rider_id = serializers.CharField(max_length=100)


class RiderPickUpOrderSerializer(serializers.Serializer):
    proof = serializers.FileField(write_only=True)


class RiderFailedPickupSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=100, required=False)


class RateRiderSerializer(serializers.Serializer):
    rating = serializers.IntegerField(max_value=5, min_value=1)
    remark = serializers.CharField(max_length=100, required=False)
    favorite_rider = serializers.BooleanField(default=False)
