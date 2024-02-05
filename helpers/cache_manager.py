from typing import Any

from django.conf import settings
from django.core.cache import cache


class CacheManager:
    """Utility class that abstracts interation with the caching engine"""

    @classmethod
    def set_key(cls, key: str, data: Any, minutes: int = None) -> None:
        timeout = None
        if minutes:
            timeout = 60 * minutes
        key = f"{settings.ENVIRONMENT}:{key}"
        cache.set(key, data, timeout=timeout)

    @classmethod
    def retrieve_key_ttl(cls, key: str) -> int:
        key = f"{settings.ENVIRONMENT}:{key}"
        return cache.ttl(key)

    @classmethod
    def retrieve_key(cls, key: str) -> Any:
        key = f"{settings.ENVIRONMENT}:{key}"
        return cache.get(key)

    @classmethod
    def delete_key(cls, key: str) -> None:
        key = f"{settings.ENVIRONMENT}:{key}"
        cache.delete(key)

    @classmethod
    def retrieve_all_cache_data(cls):
        all_cache_data = {}
        cache_keys = cache.keys(
            f"{settings.ENVIRONMENT}:*"
        )  # Retrieve all keys matching the environment prefix
        for key in cache_keys:
            data = cache.get(key)
            all_cache_data[key] = data

        return all_cache_data


class KeyBuilder:
    @staticmethod
    def user_auth_verification(email):
        return f"user:auth-verification:{email}"

    @staticmethod
    def business_user_complete_signup(session_id):
        return f"user:business-signup:{session_id}"

    @staticmethod
    def initiate_order(order_id):
        return f"customer:order:{order_id}"
