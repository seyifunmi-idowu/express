from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from rest_framework import status

from customer.service import CustomerService
from helpers.cache_manager import CacheManager, KeyBuilder
from helpers.db_helpers import generate_id
from helpers.exceptions import CustomAPIException
from helpers.googlemaps_service import GoogleMapsService
from helpers.s3_uploader import S3Uploader
from order.models import Address, Order, Vehicle
from rider.models import FavoriteRider, RiderRating
from rider.service import RiderService


class VehicleService:
    @classmethod
    def get_available_vehicles(cls):
        current_datetime = timezone.now()
        return Vehicle.objects.filter(
            status=Vehicle.STATUS[0][0],  # "ACTIVE"
            start_date__lte=current_datetime,
            end_date__gte=current_datetime,
        )

    @classmethod
    def get_vehicle(cls, vehicle_id, raise_404=True):
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if not vehicle and raise_404:
            raise CustomAPIException("Vehicle not found.", status.HTTP_404_NOT_FOUND)
        return vehicle


class MapService:
    @classmethod
    def get_info_from_address(cls, address):
        response = GoogleMapsService.get_address_details(address)
        results = response["results"]
        if len(results) < 1:
            raise CustomAPIException("Cannot locate address", status.HTTP_404_NOT_FOUND)

        results_list = [
            {
                "latitude": result.get("geometry", {}).get("location", {}).get("lat"),
                "longitude": result.get("geometry", {}).get("location", {}).get("lng"),
                "formatted_address": result.get("formatted_address"),
            }
            for result in results
        ]
        return results_list

    @classmethod
    def get_info_from_latitude_and_longitude(cls, latitude, longitude):
        response = GoogleMapsService.get_latitude_and_longitude_details(
            latitude, longitude
        )
        results = response["results"]
        if len(results) < 1:
            raise CustomAPIException("Cannot locate address", status.HTTP_404_NOT_FOUND)

        results_list = [
            {
                "latitude": result.get("geometry", {}).get("location", {}).get("lat"),
                "longitude": result.get("geometry", {}).get("location", {}).get("lng"),
                "formatted_address": result.get("formatted_address"),
            }
            for result in results
            if "street_address" in result.get("types")
        ]
        return results_list

    @classmethod
    def get_distance_between_locations(cls, start_lat_lng, end_lat_lng):
        response = GoogleMapsService.get_distance_matrix(start_lat_lng, end_lat_lng)
        if response.get("status") == "OK":
            rows = response.get("rows", [])[0]
            elements = rows.get("elements", [])[0]
            distance = elements.get("distance", {}).get("value")
            duration = elements.get("duration", {}).get("value")
            return {"distance": distance, "duration": duration}


class OrderService:
    @classmethod
    def get_order(cls, order_id, raise_404=True, **kwargs):
        order = Order.objects.filter(order_id=order_id, **kwargs).first()
        if not order and raise_404:
            raise CustomAPIException("Order not found.", status.HTTP_404_NOT_FOUND)
        return order

    @classmethod
    def get_order_qs(cls, **kwargs):
        return Order.objects.filter(**kwargs)

    @classmethod
    def get_new_order(cls, user):
        orders = Order.objects.filter(
            Q(rider__user=user, status="PENDING_RIDER_CONFIRMATION")
            | Q(rider__isnull=True, status="PENDING")
        )
        return orders

    @classmethod
    def get_completed_order(cls, request):
        created_at = request.GET.get("created_at")
        timeframe = request.GET.get("timeframe")

        order_qs = Order.objects.filter(
            rider__user=request.user, status="ORDER_COMPLETED"
        )

        if created_at:
            start_date = datetime.strptime(created_at, "%Y-%m-%d")
            end_date = start_date + timedelta(days=1)
            order_qs = order_qs.filter(created_at__range=(start_date, end_date))

        if timeframe:
            if timeframe.lower() == "today":
                today = datetime.now().date()
                order_qs = order_qs.filter(updated_at__date=today)
            elif timeframe.lower() == "yesterday":
                yesterday = datetime.now().date() - timedelta(days=1)
                order_qs = order_qs.filter(updated_at__date=yesterday)

        return order_qs

    @classmethod
    def get_current_order_qs(cls, user):
        return Order.objects.filter(
            rider__user=user,
            status__in=[
                "RIDER_ACCEPTED_ORDER",
                "RIDER_AT_PICK_UP",
                "RIDER_PICKED_UP_ORDER",
                "ORDER_ARRIVED",
            ],
        )

    @classmethod
    def get_failed_order(cls, user):
        return Order.objects.filter(rider__user=user, status__in=["ORDER_CANCELLED"])

    # @classmethod
    # def get_new_order(cls):
    #     data = CacheManager.retrieve_all_cache_data("customer:order")
    #     formatted_data = []
    #
    #     for order_id, order_data in data.items():
    #         formatted_order = {
    #             "order_id": order_data["order_id"],
    #             "status": "PENDING",
    #             "pickup": {"address": order_data["pickup"]["address"]},
    #             "delivery": {"address": order_data["delivery"]["address"]},
    #             "total_amount": order_data["total_price"],
    #             "distance": cls.get_km_in_word(order_data["total_distance"]),
    #             "duration": cls.get_time_in_word(order_data["total_duration"]),
    #         }
    #         formatted_data.append(formatted_order)
    #     return formatted_data

    @classmethod
    def create_order(cls, order_id, customer, data):
        pickup = data["pickup"]
        delivery = data["delivery"]
        total_duration = data.get("total_duration")
        total_distance = data.get("total_distance")
        stop_overs = data.get("stop_overs", [])
        vehicle_id = data.get("vehicle_id")
        payment_method = data.get("payment_method")
        payment_by = data.get("payment_by")
        timeline = data.get("timeline")

        if pickup.get("save_address"):
            cls.save_address(customer, pickup)
        if delivery.get("save_address"):
            cls.save_address(customer, delivery)
        for stop_over in stop_overs:
            if stop_over.get("save_address"):
                cls.save_address(customer, stop_over)

        order_meta_data = {
            "note_to_driver": data.get("note_to_driver"),
            "promo_code": data.get("promo_code"),
            "timeline": timeline,
        }
        return Order.objects.create(
            customer=customer,
            vehicle=VehicleService.get_vehicle(vehicle_id),
            order_id=order_id,
            status="PENDING",
            pickup_number=pickup.get("contact_phone_number", None),
            pickup_contact_name=pickup.get("contact_name", None),
            pickup_location=pickup.get("address"),
            pickup_location_longitude=pickup.get("longitude"),
            pickup_location_latitude=pickup.get("latitude"),
            delivery_number=delivery.get("contact_phone_number", None),
            delivery_contact_name=delivery.get("contact_name", None),
            delivery_location=delivery.get("address"),
            delivery_location_longitude=delivery.get("longitude"),
            delivery_location_latitude=delivery.get("latitude"),
            order_stop_overs_meta_data=stop_overs,
            total_amount=data.get("total_price"),
            tip_amount=data.get("tip_amount"),
            distance=total_distance,
            duration=total_duration,
            order_meta_data=order_meta_data,
            payment_method=payment_method,
            payment_by=payment_by,
        )

    @classmethod
    def save_address(cls, customer, data):
        Address.objects.create(
            customer=customer,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            formatted_address=data.get("address"),
        )

    @classmethod
    def generate_orderid(cls):
        import random
        import string

        return "".join(random.choices(string.ascii_lowercase + string.digits, k=10))

    @classmethod
    def get_km_in_word(cls, distance_in_meters):
        distance_in_km = int(distance_in_meters) / 1000
        formatted_distance = "{:.1f}".format(distance_in_km)
        return f"{formatted_distance} km"

    @classmethod
    def get_time_in_word(cls, time_in_seconds):
        time_in_minutes = int(time_in_seconds) / 60
        formatted_time = "{:.0f}".format(time_in_minutes)
        return f"{formatted_time} mins"

    @classmethod
    def initiate_order(cls, user, data):
        pickup = data["pickup"]
        delivery = data["delivery"]
        stop_overs = data.get("stop_overs", [])
        vehicle_id = data["vehicle_id"]
        pickup_latitude = pickup["latitude"]
        pickup_longitude = pickup["longitude"]
        delivery_latitude = delivery["latitude"]
        delivery_longitude = delivery["longitude"]
        total_price = 0
        total_distance = 0
        total_duration = 0
        timeline = []
        index = 1

        pickup_address_info = MapService.get_info_from_latitude_and_longitude(
            pickup_latitude, pickup_longitude
        )
        if len(pickup_address_info) < 1:
            raise CustomAPIException(
                "Unable to locate pickup address", status.HTTP_404_NOT_FOUND
            )
        pickup.update({"address": pickup_address_info[0].get("formatted_address")})
        delivery_address_info = MapService.get_info_from_latitude_and_longitude(
            delivery_latitude, delivery_longitude
        )
        if len(pickup_address_info) < 1:
            raise CustomAPIException(
                "Unable to locate delivery address", status.HTTP_404_NOT_FOUND
            )
        delivery.update({"address": delivery_address_info[0].get("formatted_address")})

        if stop_overs:
            current_location = pickup
            for stop_over in stop_overs:
                stop_over_latitude = stop_over.get("latitude")
                stop_over_longitude = stop_over.get("longitude")
                stop_over_address_info = MapService.get_info_from_latitude_and_longitude(
                    stop_over_latitude, stop_over_longitude
                )
                if len(pickup_address_info) < 1:
                    raise CustomAPIException(
                        "Unable to locate stop over address", status.HTTP_404_NOT_FOUND
                    )
                stop_over.update(
                    {"address": stop_over_address_info[0].get("formatted_address")}
                )

                distance_and_duration = MapService.get_distance_between_locations(
                    f"{current_location.get('latitude')},{current_location.get('longitude')}",
                    f"{stop_over_latitude},{stop_over_longitude}",
                )
                total_distance += distance_and_duration.get("distance")
                total_duration += distance_and_duration.get("duration")

                price = cls.calculate_distance_price(
                    distance_and_duration.get("distance"),
                    distance_and_duration.get("duration"),
                    vehicle_id,
                )
                timeline.append(
                    {
                        "index": index,
                        "from": {
                            "latitude": current_location.get("latitude"),
                            "longitude": current_location.get("longitude"),
                        },
                        "to": {
                            "latitude": stop_over_latitude,
                            "longitude": stop_over_longitude,
                        },
                        "price": price,
                        "total_price": total_price + price,
                        **distance_and_duration,
                    }
                )
                total_price += price
                current_location = stop_over
                index += 1

            distance_and_duration = MapService.get_distance_between_locations(
                f"{current_location.get('latitude')},{current_location.get('longitude')}",
                f"{delivery.get('latitude')},{delivery.get('longitude')}",
            )
            total_distance += distance_and_duration.get("distance")
            total_duration += distance_and_duration.get("duration")

            price = cls.calculate_distance_price(
                distance_and_duration.get("distance"),
                distance_and_duration.get("duration"),
                vehicle_id,
            )
            timeline.append(
                {
                    "index": index,
                    "from": {
                        "latitude": current_location.get("latitude"),
                        "longitude": current_location.get("longitude"),
                    },
                    "to": {
                        "latitude": delivery.get("latitude"),
                        "longitude": delivery.get("longitude"),
                    },
                    "price": price,
                    "total_price": total_price + price,
                    **distance_and_duration,
                }
            )
            total_price += price

        else:
            distance_and_duration = MapService.get_distance_between_locations(
                (pickup_latitude, pickup_longitude),
                (delivery_latitude, delivery_longitude),
            )
            if distance_and_duration.get("distance") is None:
                raise CustomAPIException(
                    "Unable to process, please check that the address or (longitude and latitude) are correct",
                    status.HTTP_400_BAD_REQUEST,
                )
            total_distance += distance_and_duration.get("distance")
            total_duration += distance_and_duration.get("duration")

            total_price += cls.calculate_distance_price(
                distance_and_duration["distance"],
                distance_and_duration["duration"],
                vehicle_id,
            )
            timeline.append(
                {
                    "index": index,
                    "from": {
                        "latitude": pickup_latitude,
                        "longitude": pickup_longitude,
                    },
                    "to": {
                        "latitude": delivery_latitude,
                        "longitude": delivery_longitude,
                    },
                    "vehicle_id": vehicle_id,
                    "price": total_price,
                    "total_price": total_price,
                    **distance_and_duration,
                }
            )

        order_id = cls.generate_orderid()
        data = {
            "user_id": user.id,
            "order_id": order_id,
            "pickup": pickup,
            "delivery": delivery,
            "stop_overs": stop_overs,
            "total_price": round(total_price, 2),
            "vehicle_id": vehicle_id,
            "total_distance": total_distance,
            "total_duration": total_duration,
            "timeline": timeline,
        }
        key_builder = KeyBuilder.initiate_order(order_id)
        CacheManager.set_key(key_builder, data, minutes=120)
        data.pop("timeline")
        data.pop("vehicle_id")
        data.pop("user_id")
        data["pickup"].pop("save_address")
        data["delivery"].pop("save_address")
        for stop_over in data["stop_overs"]:
            stop_over.pop("save_address")

        return data

    @classmethod
    def calculate_distance_price(cls, distance, duration, vehicle_id):
        vehicle = VehicleService.get_vehicle(vehicle_id=vehicle_id)
        base_fare = vehicle.base_fare
        price_per_km_0_5 = vehicle.km_5_below_fare
        price_per_km_5_above = vehicle.km_5_above_fare
        # price_per_minute = vehicle.price_per_minute
        price_per_minute = 80

        # Convert distance from meters to kilometers
        distance_km = distance / 1000

        if distance_km <= 5:
            price_distance = base_fare + distance_km * price_per_km_0_5
        else:
            price_distance = (
                base_fare
                + 5 * price_per_km_0_5
                + (distance_km - 5) * price_per_km_5_above
            )

        # Calculate the price based on the duration
        price_duration = duration / 60 * price_per_minute

        # Total price is the sum of distance and duration prices
        total_price = price_distance + price_duration

        return total_price

    @classmethod
    def place_order(cls, user, order_id, request):
        key_builder = KeyBuilder.initiate_order(order_id)
        order_data = CacheManager.retrieve_key(key_builder)
        if not order_data or order_data.get("user_id") != user.id:
            raise CustomAPIException("Order not found.", status.HTTP_404_NOT_FOUND)

        if request["payment_method"] == "WALLET":
            user_wallet = user.get_user_wallet()
            if user_wallet.balance < order_data["total_price"]:
                raise CustomAPIException(
                    "You don't have sufficient in you wallet to place order. Kindly fund you wallet.",
                    status.HTTP_400_BAD_REQUEST,
                )

        order_data.update(request)
        longitude = order_data.get("pickup", {}).get("longitude")
        latitude = order_data.get("pickup", {}).get("latitude")
        customer = CustomerService.get_customer(user=user)
        cls.create_order(order_id, customer, order_data)
        cls.notify_riders_around_location(longitude, latitude)
        CacheManager.delete_key(key_builder)
        return True

    @classmethod
    def notify_riders_around_location(cls, longitude, latitude):
        # TODO: check not busy, active riders within 5km and notify
        pass

    @classmethod
    def add_rider_tip(cls, user, order_id, tip_amount):
        order = cls.get_order(order_id, customer__user=user)
        order.tip_amount += tip_amount
        order.save()
        return True

    @classmethod
    def add_order_timeline_entry(cls, order, order_status, **kwargs):
        order_timeline = order.order_timeline or []
        order_timeline.append(
            {
                "status": order_status,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **kwargs,
            }
        )
        order.order_timeline = order_timeline
        order.save()

    @classmethod
    def assign_rider_to_order(cls, user, order_id, rider_id):
        order = cls.get_order(order_id, customer__user=user)
        if order.status != "PENDING":
            raise CustomAPIException("Order is not pending", status.HTTP_404_NOT_FOUND)
        if order.rider is not None:
            raise CustomAPIException(
                "Rider already assigned to ride", status.HTTP_404_NOT_FOUND
            )

        favourite_rider = FavoriteRider.objects.filter(
            rider__id=rider_id, customer__user=user
        ).first()
        if favourite_rider is None:
            raise CustomAPIException(
                "Rider not a part of your favourite riders.", status.HTTP_404_NOT_FOUND
            )

        cls.add_order_timeline_entry(order, "CUSTOMER_ASSIGN_RIDER")
        cls.add_order_timeline_entry(order, "PENDING_RIDER_CONFIRMATION")

        order.rider = favourite_rider.rider
        order.status = "PENDING_RIDER_CONFIRMATION"
        order.save()

    @classmethod
    def rate_rider(cls, user, order_id, **kwargs):
        order = cls.get_order(order_id, customer__user=user)
        favorite_rider = kwargs.get("favorite_rider", False)
        rating = kwargs.get("rating")
        remark = kwargs.get("remark", "")
        RiderRating.objects.create(
            rider=order.rider, customer=order.customer, remark=remark, rating=rating
        )
        if favorite_rider:
            FavoriteRider.objects.create(rider=order.rider, customer=order.customer)
        return True

    @classmethod
    def rider_accept_customer_order(cls, user, order_id):
        order = cls.get_order(order_id)
        pass_rider = False
        if order.rider is None and order.status == "PENDING":
            pass_rider = True
        if (
            order.rider
            and order.rider.user == user
            and order.status == "PENDING_RIDER_CONFIRMATION"
        ):
            pass_rider = True
        if not pass_rider:
            raise CustomAPIException("Cannot accept order.", status.HTTP_404_NOT_FOUND)
        rider = RiderService.get_rider(user=user)
        cls.add_order_timeline_entry(order, "RIDER_ACCEPTED_ORDER")

        order.rider = rider
        order.status = "RIDER_ACCEPTED_ORDER"
        order.save()
        return order

    @classmethod
    def rider_at_pickup(cls, order_id, user):
        order = cls.get_order(order_id, rider__user=user)
        cls.add_order_timeline_entry(order, "RIDER_AT_PICK_UP")
        order.status = "RIDER_AT_PICK_UP"
        order.save()

    @classmethod
    def rider_at_order_pickup(cls, order_id, user, file):
        order = cls.get_order(order_id, rider__user=user)

        file_name = file.name
        file_url = S3Uploader(append_folder=f"/order/{order_id}").upload_file_object(
            file, file_name
        )
        cls.add_order_timeline_entry(
            order, "RIDER_PICKED_UP_ORDER", **{"proof_of_pickup_url": file_url}
        )
        order.status = "RIDER_PICKED_UP_ORDER"
        order.save()

    @classmethod
    def rider_failed_pickup(cls, order_id, user, reason):
        order = cls.get_order(order_id, rider__user=user)

        cls.add_order_timeline_entry(order, "FAILED_PICKUP", **{"reason": reason})
        cls.add_order_timeline_entry(order, "ORDER_CANCELLED")
        order.status = "ORDER_CANCELLED"
        order.save()

    @classmethod
    def rider_at_destination(cls, order_id, user):
        order = cls.get_order(order_id, rider__user=user)
        cls.add_order_timeline_entry(order, "ORDER_ARRIVED")
        order.status = "ORDER_ARRIVED"
        order.save()

    @classmethod
    def rider_made_delivery(cls, order_id, user, file):
        order = cls.get_order(order_id, rider__user=user)

        file_name = file.name
        file_url = S3Uploader(append_folder=f"/order/{order_id}").upload_file_object(
            file, file_name
        )
        cls.add_order_timeline_entry(
            order, "ORDER_DELIVERED", **{"proof_of_delivery_url": file_url}
        )
        order.delivery_time = timezone.now()
        order.status = "ORDER_DELIVERED"
        order.save()
        if order.payment_method == "WALLET":
            cls.debit_customer(order)

        return True

    @classmethod
    def rider_received_payment(cls, order_id, user):
        order = cls.get_order(order_id, rider__user=user)
        cls.add_order_timeline_entry(order, "ORDER_COMPLETED")
        order.paid = True
        order.status = "ORDER_COMPLETED"
        order.fele_amount = order.total_amount * Decimal(settings.FELE_CHARGE / 100)
        order.save()
        return order

    @classmethod
    def debit_customer(cls, order):
        from helpers.paystack_service import PaystackService
        from wallet.service import CardService, TransactionService

        amount = order.total_amount
        customer_user = order.customer.user
        rider_user = order.rider.user
        customer_user_wallet = customer_user.get_user_wallet()
        transaction_obj = None
        made_payment = False
        if customer_user_wallet.balance > amount:
            # debit wallet and mark as completed
            reference = generate_id()
            customer_user_wallet.withdraw(amount)
            transaction_obj = TransactionService.create_transaction(
                transaction_type="DEBIT",
                transaction_status="SUCCESS",
                amount=Decimal(amount),
                user=customer_user,
                reference=reference,
                pssp="IN_HOUSE",
                payment_category="CUSTOMER_PAY_RIDER",
            )
            made_payment = True

        else:
            # debit card
            user_card = CardService.get_user_cards(customer_user).first()
            if user_card:
                response = PaystackService.charge_card(
                    customer_user.email, amount, user_card.card_auth
                )
                if response["status"] and response["data"]["status"] == "success":
                    reference = response["data"]["reference"]
                    transaction_obj = TransactionService.create_transaction(
                        transaction_type="DEBIT",
                        transaction_status="SUCCESS",
                        amount=Decimal(amount),
                        user=customer_user,
                        reference=reference,
                        pssp="PAYSTACK",
                        payment_category="CUSTOMER_PAY_RIDER",
                    )
                    made_payment = True

        if made_payment:
            cls.add_order_timeline_entry(order, "ORDER_COMPLETED")
            order.paid = True
            order.status = "ORDER_COMPLETED"
            order.fele_amount = amount * Decimal(settings.FELE_CHARGE / 100)
            order.paid_fele = True
            order.save()

            rider_user_wallet = rider_user.get_user_wallet()
            TransactionService.create_transaction(
                transaction_type="CREDIT",
                transaction_status="SUCCESS",
                amount=Decimal(amount),
                user=rider_user,
                reference=transaction_obj.reference,
                pssp=transaction_obj.pssp,
                payment_category="CUSTOMER_PAY_RIDER",
                wallet_id=rider_user_wallet.id,
            )
            rider_user_wallet.deposit(order.total_amount - order.fele_amount)

            # TODO: check if rider has outstanding and deduct it

        return made_payment
