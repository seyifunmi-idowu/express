from typing import Dict, List, Union

from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class CustomFieldValidationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An error occurred with this field."

    def __init__(
        self, detail: Union[List, Dict, str], field: str, status_code: int
    ) -> None:
        self.status_code = status_code if status_code else self.status_code
        detail = detail if detail is not None else self.default_detail

        self.detail = {"errors": {field: [force_str(detail)]}}


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = (
        "We are unable to process your request at this time. Please try again."
    )

    def __init__(self, detail: Union[List, Dict, str], status_code: int) -> None:
        self.status_code = status_code if status_code else self.status_code
        message = detail if detail is not None else self.default_message
        self.detail = {"message": force_str(message)}


def custom_exception_handler(exc, context):

    handlers = {
        "Http404": _handle_404_error,
        "InvalidToken": _handle_invalid_token_error,
        "PermissionDenied": _handle_403_error,
    }

    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return _handle_generic_error(exc, context, response)


def _handle_404_error(exc, context, response):

    response.data = {
        "message": "Object not found."  # TODO: We can improve this description
    }

    return response


def _handle_invalid_token_error(exc, context, response):

    response.data = {"message": "Token is invalid or expired"}

    return response


def _handle_403_error(exc, context, response):

    response.data = {"message": "You are not authorized to perform this action."}

    return response


def _handle_generic_error(exc, context, response):
    try:
        if response.data.get("detail") and not response.data.get("message"):
            response.data = {"message": str(response.data.get("detail"))}
    except Exception:
        pass
    return response
