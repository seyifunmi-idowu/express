from django.conf import settings
from rest_framework.permissions import BasePermission


class IsPaystack(BasePermission):
    def has_permission(self, request, view):
        from helpers.hash_method import hmac_sha512
        from helpers.ip_lookup import _ip_address_is_valid, get_ip_address
        from helpers.logger import CustomLogging

        paystack_hash = request.headers.get("x-paystack-signature")
        data = request.data
        ip_address = get_ip_address(request)
        if (
            not _ip_address_is_valid(ip_address)
            or ip_address not in settings.PAYSTACK_WHITELISTED_IP
        ):
            extra = {
                "data": str(data),
                "IP": ip_address,
                "info": "IP address not whitelisted",
            }
            CustomLogging.error(
                "Error occurred on Paystack webhook listener", extra=extra
            )
            return False
        hashed_data = hmac_sha512(data, settings.PAYSTACK_SECRET_KEY)
        if hashed_data != paystack_hash:
            extra = {
                "data": str(data),
                "paystack_hash": paystack_hash,
                "info": "Signature match failed",
            }
            CustomLogging.error(
                "Error occurred on Paystack webhook listener", extra=extra
            )
            return False
        env = settings.ENVIRONMENT
        if env == "production" and data.get("data", {}).get("domain") != "live":
            extra = {
                "data": str(data),
                "environment": env,
                "info": "Domain check failed.",
            }
            CustomLogging.error(
                "Error occurred on Paystack webhook listener", extra=extra
            )
            return False
        return True
