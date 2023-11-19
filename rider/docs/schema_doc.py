from drf_yasg import openapi

RIDER_INFO = {
    "id": "1f1d831988564d0eb6adcf6a5bbcb0a0",
    "user": {
        "id": "3979c56f95d4474580f466b7123e955f",
        "first_name": "John",
        "last_name": "Mark",
        "email": "johnmark@yahoo.com",
        "email_verified": False,
        "phone_number": "+2348105474517",
        "phone_verified": True,
        "street_address": None,
        "city": None,
        "last_login": "2023-10-04T07:17:48.924120Z",
        "is_rider": True,
        "is_customer": False,
        "display_name": "John Mark",
    },
    "status": "UNAPPROVED",
    "vehicle_type": "CAR",
    "vehicle_make": None,
    "vehicle_model": None,
    "vehicle_plate_number": None,
    "vehicle_color": None,
    "rider_info": None,
    "city": None,
    "avatar_url": None,
    "vehicle_photos": [],
}
UNAUTHENTICATED = {
    "application/json": {"message": "Token is invalid or expired"}  # type: ignore
}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Rider sign up successful"}
}

EMAIL_REGISTRATION_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["Enter a valid email address."],
            "vehicle_type": ["This field is required."],
        }
    }
}

EMAIL_REGISTRATION_EXISITING_USER_RESPONSE = {
    "application/json": {
        "errors": {"email": ["A user has already registered with this email address"]}
    }
}

RIDER_REGISTRATION_RESPONSES = {
    201: openapi.Response(
        description="Created User", examples=REGISTRATION_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=EMAIL_REGISTRATION_BAD_INPUT_RESPONSE
    ),
    409: openapi.Response(
        description="Existing User", examples=EMAIL_REGISTRATION_EXISITING_USER_RESPONSE
    ),
}

LOGIN_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "rider": RIDER_INFO,
            "token": {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9....",
            },
        }
    },
    "message": "",
}

LOGIN_WITH_EMAIL_UNAUTHORISED_RESPONSE = {
    "application/json": {"message": "Email or password is not correct"}
}

LOGIN_WITH_EMAIL_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "email": ["This field is required."],
            "password": ["This field is required."],
        }
    }
}
LOGIN_RESPONSES = {
    200: openapi.Response(
        description="Successful Login", examples=LOGIN_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=LOGIN_WITH_EMAIL_BAD_INPUT_RESPONSE
    ),
    401: openapi.Response(
        description="Invalid Credentials",
        examples=LOGIN_WITH_EMAIL_UNAUTHORISED_RESPONSE,
    ),
}
RIDER_INFO_SUCCESS_RESPONSE = {
    "application/json": {"data": RIDER_INFO, "message": "Rider info"}
}
RIDER_INFO_RESPONSE = {
    200: openapi.Response(
        description="Rider information", examples=RIDER_INFO_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
SUBMIT_KYC_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "status": "UNAPPROVED",
            "vehicle_photo": {
                "status": "verified",
                "files": [
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/vehicle_photo/ea0c46dc891d4eb2b6524768b.pdf",
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/vehicle_photo/bb96efdd025.pdf",
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/vehicle_photo/9a465cdf1be4cf91c01e.pdf",
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/vehicle_photo/1bbd4cea5b1cf952d1.pdf",
                ],
            },
            "passport_photo": {
                "status": "unverified",
                "files": [
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/passport_photo/0d8d5e05394fea.jpeg",
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/passport_photo/897997d19b033b46a.jpeg",
                ],
            },
            "government_id": {
                "status": "unverified",
                "files": [
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/government_id/6c6cf3458aecc44b20e380a7.jpeg",
                    "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/government_id/bae45540c4484bc3371a30f51d.png",
                ],
            },
            "guarantor_letter": {"status": "unverified", "files": []},
            "address_verification": {"status": "unverified", "files": []},
        },
        "message": "Kyc submitted",
    }
}
SUBMIT_KYC_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "vehicle_type": ["This field is required."],
            "vehicle_plate_number": ["This field is required."],
        }
    }
}
SUBMIT_KYC_RESPONSE = {
    200: openapi.Response(
        description="Kyc submitted", examples=SUBMIT_KYC_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=SUBMIT_KYC_BAD_INPUT_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
UPLOAD_DOCUMENT_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Document(s) uploaded"}
}
UPLOAD_DOCUMENT_BAD_INPUT_RESPONSE = {
    "application/json": {
        "errors": {
            "document_type": ["This field is required."],
            "documents": ["This field is required."],
        }
    }
}
UPLOAD_DOCUMENT_RESPONSE = {
    200: openapi.Response(
        description="Kyc submitted", examples=SUBMIT_KYC_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad Input", examples=UPLOAD_DOCUMENT_BAD_INPUT_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
KYC_INFO_RESPONSE = {
    200: openapi.Response(
        description="Kyc submitted", examples=SUBMIT_KYC_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
VEHICLE_INFO_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "vehicle_type": "CAR",
            "vehicle_make": None,
            "vehicle_model": None,
            "vehicle_plate_number": "eky24sky",
            "vehicle_color": "red",
            "driver_license": {"status": "unverified", "files": []},
            "insurance_certificate": {"status": "unverified", "files": []},
        },
        "message": "Kyc submitted",
    }
}
VEHICLE_INFO_RESPONSE = {
    200: openapi.Response(
        description="Vehicle information", examples=VEHICLE_INFO_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}

UPDATE_VEHICLE_RESPONSE = {
    200: openapi.Response(
        description="Vehicle information updated",
        examples=VEHICLE_INFO_SUCCESS_RESPONSE,
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
