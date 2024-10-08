from rest_framework import permissions

from helpers.validate_user import (
    validate_admin,
    validate_approved_rider,
    validate_business,
    validate_customer,
    validate_deactivated_user,
    validate_rider,
    validate_user,
    validate_verified_user,
)


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


class IsRider(permissions.BasePermission):
    """
    Custom permission to allow only riders make this request
    """

    def has_permission(self, request, view):
        return validate_rider(request.user)


class IsCustomer(permissions.BasePermission):
    """
    Custom permission to allow only customers make this request
    """

    def has_permission(self, request, view):
        return validate_customer(request.user)


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow only customers make this request
    """

    def has_permission(self, request, view):
        return validate_admin(request.user)


class IsApprovedRider(permissions.BasePermission):
    """
    Custom permission to allow only approved riders make this request
    """

    def has_permission(self, request, view):
        return validate_approved_rider(request.user)


class IsBusiness(permissions.BasePermission):
    """
    Custom permission to allow only business make this request
    """

    def has_permission(self, request, view):
        return validate_business(request.user)
