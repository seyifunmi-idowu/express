from rest_framework import serializers

from order.models import Order, OrderTimeline, Vehicle


class RetrieveVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "name", "note", "file_url")


class OrderTimelineSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = OrderTimeline
        fields = ("status", "proof_url", "reason", "date")

    def get_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")


class GetCustomerOrderSerializer(serializers.ModelSerializer):
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    rider = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("order_id", "status", "pickup", "delivery", "rider")

    def get_pickup(self, obj):
        return {
            "address": obj.pickup_name,
            "time": obj.get_pick_up_time(),
            "name": obj.pickup_name,
        }

    def get_rider(self, obj):
        if obj.rider:
            return {
                "name": obj.rider.display_name,
                "contact": obj.rider.user.phone_number,
                "avatar_url": obj.rider.photo_url(),
                "rating": obj.rider.rating,
                "vehicle": obj.rider.vehicle.name,
                "vehicle_type": obj.rider.vehicle_type,
                "vehicle_make": obj.rider.vehicle_make,
                "vehicle_model": obj.rider.vehicle_model,
                "vehicle_plate_number": obj.rider.vehicle_plate_number,
                "vehicle_color": obj.rider.vehicle_color,
            }
        return None

    def get_delivery(self, obj):
        return {
            "address": obj.delivery_name,
            "time": obj.get_delivery_time(),
            "name": obj.delivery_name,
        }


class OrderHistorySerializer(serializers.ModelSerializer):
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    rider = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "status",
            "total_amount",
            "pickup",
            "delivery",
            "rider",
            "created_at",
        )

    def get_pickup(self, obj):
        return {"address": obj.pickup_location, "name": obj.pickup_name}

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%B-%d %H:%M:%S")

    def get_delivery(self, obj):
        return {"address": obj.delivery_location, "name": obj.delivery_name}

    def get_rider(self, obj):
        if obj.rider:
            return {
                "id": obj.rider.id,
                "name": obj.rider.display_name,
                "contact": obj.rider.user.phone_number,
                "avatar_url": obj.rider.photo_url(),
                "rating": obj.rider.rating,
                "vehicle": obj.rider.vehicle.name,
                "vehicle_type": obj.rider.vehicle_type,
                "vehicle_make": obj.rider.vehicle_make,
                "vehicle_model": obj.rider.vehicle_model,
                "vehicle_plate_number": obj.rider.vehicle_plate_number,
                "vehicle_color": obj.rider.vehicle_color,
            }
        return None


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
        return {"address": obj.pickup_location, "name": obj.pickup_name}

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_delivery(self, obj):
        return {"address": obj.delivery_location, "name": obj.delivery_name}

    def get_assigned_by_customer(self, obj):
        return obj.status == "PENDING_RIDER_CONFIRMATION"


class GetCurrentOrder(GetOrderSerializer):
    contact = serializers.SerializerMethodField()
    note_to_rider = serializers.SerializerMethodField()
    order_by = serializers.SerializerMethodField()

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
            "order_by",
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
        if obj.pickup_location:
            split_address = obj.pickup_location.split(", ", 1)
        else:
            split_address = [obj.pickup_name]

        return {
            "address": obj.pickup_location,
            "longitude": obj.pickup_location_longitude,
            "latitude": obj.pickup_location_latitude,
            "short_address": obj.pickup_name if obj.pickup_name else split_address[0],
            "complete_address": split_address[1] if len(split_address) > 1 else "",
            "contact": obj.pickup_number,
            "contact_name": obj.pickup_contact_name,
            "time": obj.get_pick_up_time(),
            "name": obj.pickup_name,
        }

    def get_delivery(self, obj):
        if obj.delivery_location:
            split_address = obj.delivery_location.split(", ", 1)
        else:
            split_address = [obj.delivery_name]

        return {
            "address": obj.delivery_location,
            "longitude": obj.delivery_location_longitude,
            "latitude": obj.delivery_location_latitude,
            "short_address": obj.delivery_name
            if obj.delivery_name
            else split_address[0],
            "complete_address": split_address[1] if len(split_address) > 1 else "",
            "contact": obj.delivery_number,
            "contact_name": obj.delivery_contact_name,
            "time": obj.get_delivery_time(),
            "name": obj.delivery_name,
        }

    def get_distance(self, obj):
        from order.service import OrderService

        return OrderService.get_km_in_word(obj.distance)

    def get_duration(self, obj):
        from order.service import OrderService

        return OrderService.get_time_in_word(obj.duration)

    def get_note_to_rider(self, obj):
        return obj.order_meta_data.get("note_to_driver", "")

    def get_order_by(self, obj):
        order_by = obj.order_by
        order_by_mapper = {"CUSTOMER": obj.customer, "BUSINESS": obj.business}
        return order_by_mapper[order_by].display_name


class CustomerOrderSerializer(serializers.ModelSerializer):
    rider = serializers.SerializerMethodField()
    rider_contact = serializers.SerializerMethodField()
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    stopover = serializers.SerializerMethodField()
    note_to_driver = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "status",
            "payment_method",
            "payment_by",
            "rider",
            "rider_contact",
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
            "rating",
        )

    def get_pickup(self, obj):
        return {
            "latitude": obj.pickup_location_latitude,
            "longitude": obj.pickup_location_longitude,
            "address": obj.pickup_location,
            "contact_name": obj.pickup_contact_name,
            "contact_phone_number": obj.pickup_number,
            "name": obj.pickup_name,
        }

    def get_delivery(self, obj):
        return {
            "latitude": obj.delivery_location_latitude,
            "longitude": obj.delivery_location_longitude,
            "address": obj.delivery_location,
            "contact_name": obj.delivery_contact_name,
            "contact_phone_number": obj.delivery_number,
            "name": obj.delivery_name,
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
        return obj.order_meta_data.get("note_to_driver", "")

    def get_timeline(self, obj):
        from order.service import OrderService

        order_timeline = OrderService.get_order_timeline(obj)
        return OrderTimelineSerializer(order_timeline, many=True).data

    def get_distance(self, obj):
        from order.service import OrderService

        return OrderService.get_km_in_word(obj.distance)

    def get_duration(self, obj):
        from order.service import OrderService

        return OrderService.get_time_in_word(obj.duration)

    def get_rider_contact(self, obj):
        if obj.rider:
            return obj.rider.user.phone_number
        return None

    def get_rating(self, obj):
        from rider.models import RiderRating

        rating = RiderRating.objects.filter(
            rider=obj.rider, customer=obj.customer
        ).first()
        if rating:
            return {
                "rating": rating.rating,
                "created_at": rating.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            return {"rating": None, "created_at": None}

    def get_rider(self, obj):
        if obj.rider:
            return {
                "name": obj.rider.display_name,
                "contact": obj.rider.user.phone_number,
                "avatar_url": obj.rider.photo_url(),
                "rating": obj.rider.rating,
                "vehicle": obj.rider.vehicle.name,
                "vehicle_type": obj.rider.vehicle_type,
                "vehicle_make": obj.rider.vehicle_make,
                "vehicle_model": obj.rider.vehicle_model,
                "vehicle_plate_number": obj.rider.vehicle_plate_number,
                "vehicle_color": obj.rider.vehicle_color,
            }
        return None


class RiderOrderSerializer(serializers.ModelSerializer):
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
    stopover = serializers.SerializerMethodField()
    note_to_driver = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()

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
            "contact",
        )

    def get_pickup(self, obj):
        if obj.pickup_location:
            split_address = obj.pickup_location.split(", ", 1)
        else:
            split_address = [obj.pickup_name]

        return {
            "longitude": obj.pickup_location_longitude,
            "latitude": obj.pickup_location_latitude,
            "address": obj.pickup_location,
            "short_address": split_address[0],
            "complete_address": split_address[1] if len(split_address) > 1 else "",
            "contact_phone_number": obj.pickup_number,
            "contact_name": obj.pickup_contact_name,
            "time": obj.get_pick_up_time(),
            "name": obj.pickup_name,
        }

    def get_delivery(self, obj):
        if obj.delivery_location:
            split_address = obj.delivery_location.split(", ", 1)
        else:
            split_address = [obj.delivery_name]
        return {
            "address": obj.delivery_location,
            "longitude": obj.delivery_location_longitude,
            "latitude": obj.delivery_location_latitude,
            "short_address": split_address[0],
            "complete_address": split_address[1] if len(split_address) > 1 else "",
            "contact_phone_number": obj.delivery_number,
            "contact_name": obj.delivery_contact_name,
            "time": obj.get_delivery_time(),
            "name": obj.delivery_name,
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


class SearchAddressSerializer(serializers.Serializer):
    address = serializers.CharField(required=True)


class GetAddressInfoSerializer(serializers.Serializer):
    address = serializers.CharField(required=False)
    latitude = serializers.CharField(max_length=50, required=False)
    longitude = serializers.CharField(max_length=50, required=False)

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
    # favorite_rider = serializers.BooleanField(default=False)
    promo_code = serializers.CharField(max_length=20, required=False)


class PlaceBusinessOrderSerializer(serializers.Serializer):
    note_to_driver = serializers.CharField(max_length=500, required=False)


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


class CustomerCancelOrder(RiderFailedPickupSerializer):
    pass


class BusinessOrderSerializer(serializers.ModelSerializer):
    rider = serializers.SerializerMethodField()
    pickup = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()
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
            "rider",
            "pickup",
            "delivery",
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

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_note_to_driver(self, obj):
        return obj.order_meta_data.get("note_to_driver", "")

    def get_timeline(self, obj):
        from order.service import OrderService

        order_timeline = OrderService.get_order_timeline(obj)
        return OrderTimelineSerializer(order_timeline, many=True).data

    def get_distance(self, obj):
        from order.service import OrderService

        return OrderService.get_km_in_word(obj.distance)

    def get_duration(self, obj):
        from order.service import OrderService

        return OrderService.get_time_in_word(obj.duration)

    def get_rider(self, obj):
        if obj.rider:
            return {
                "name": obj.rider.display_name,
                "contact": obj.rider.user.phone_number,
                "avatar_url": obj.rider.photo_url(),
                "rating": obj.rider.rating,
                "vehicle": obj.rider.vehicle.name,
                "vehicle_type": obj.rider.vehicle_type,
                "vehicle_make": obj.rider.vehicle_make,
                "vehicle_model": obj.rider.vehicle_model,
                "vehicle_plate_number": obj.rider.vehicle_plate_number,
                "vehicle_color": obj.rider.vehicle_color,
            }
        return None
