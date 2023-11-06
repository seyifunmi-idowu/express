import ipaddress

import ipapi
from django.conf import settings

from helpers.cache_manager import CacheManager
from helpers.logger import CustomLogging


def lookup_ip_information(ip_address):
    try:
        if settings.ENABLED_IP_LOOKUP and _ip_address_is_valid(ip_address):
            cached_ip_details = CacheManager.retrieve_key(f"lookup:ip:{ip_address}")
            if not cached_ip_details:
                details = ipapi.location(ip=ip_address, output="json")
                CacheManager.set_key(f"lookup:ip:{ip_address}", details, 3600)
            else:
                details = cached_ip_details
        else:
            details = {}
    except Exception as e:
        details = {}
        extra = {"errors": str(e)}
        CustomLogging.error(
            "Error occurred on: `helpers/ip_lookup.py:lookup_ip_information`",
            extra=extra,
        )
    return details


def _ip_address_is_valid(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def get_ip_address(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_adress = x_forwarded_for.split(",")[0]
    else:
        ip_adress = request.META.get("REMOTE_ADDR")
    return ip_adress
