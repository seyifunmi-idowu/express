from rest_framework import permissions

from helpers.validate_user import validate_user, validate_verified_user, validate_deactivated_user


class IsAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow only active and authenticated users
    """

    def has_permission(self, request, view):
        return validate_user(request.user)


class IsNotDeactivatedUser(permissions.BasePermission):
    """
    Custom permission to prevent DEACTIVATED_USER user type from logging in
    """

    def has_permission(self, request, view):
        return validate_deactivated_user(request)


class IsVerifiedUser(permissions.BasePermission):
    """
    Custom permission to check for a verified user
    """

    def has_permission(self, request, view):
        return validate_verified_user(request.user)
