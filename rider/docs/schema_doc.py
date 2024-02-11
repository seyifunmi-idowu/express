from drf_yasg import openapi

PERIOD = openapi.Parameter(
    "timeframe",
    openapi.IN_QUERY,
    description="Filter performance by period, yesterday or today",
    type=openapi.TYPE_STRING,
    enum=["today", "yesterday", "week", "month"],
)
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
        "wallet_balance": 1000.0,
    },
    "status": "UNAPPROVED",
    "vehicle": "CAR (Sedan)",
    "vehicle_make": None,
    "vehicle_model": None,
    "vehicle_plate_number": None,
    "vehicle_color": None,
    "rider_info": None,
    "city": None,
    "avatar_url": None,
    "vehicle_photos": [],
    "total_orders": 5,
    "total_earns": 8926.59,
    "review_count": 1,
}
UNAUTHENTICATED = {
    "application/json": {"message": "Token is invalid or expired"}  # type: ignore
}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

REGISTRATION_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Rider sign up successful"}
}

EMAIL_REGISTRATION_BAD_INPUT_RESPONSE = {
    "application/json": {"errors": {"email": ["Enter a valid email address."]}}
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
OTP_RESENT_SUCCESS_RESPONSE = {"application/json": {"data": {}, "message": "Otp sent"}}
EMAIL_REGISTRATION_NONE_EXISITING_USER_RESPONSE = {
    "application/json": {"errors": {"email": ["User with email address not found"]}}
}
RIDER_RESEND_OTP_RESPONSES = {
    201: openapi.Response(description="Otp sent", examples=OTP_RESENT_SUCCESS_RESPONSE),
    400: openapi.Response(
        description="Bad Input", examples=EMAIL_REGISTRATION_BAD_INPUT_RESPONSE
    ),
    409: openapi.Response(
        description="Existing User",
        examples=EMAIL_REGISTRATION_NONE_EXISITING_USER_RESPONSE,
    ),
}

LOGIN_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            **RIDER_INFO,  # type: ignore
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
AVAILABLE_CITIES_RESPONSE = {
    200: openapi.Response(
        description="Available cities",
        examples={
            "application/json": {
                "data": {"available_cities": ["MAKURDI", "GBOKO", "OTUKPO"]},
                "message": "Available cities",
            }
        },
    )
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
RIDER_HOME_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "id": "2c4eccb6025d4c7693c5b9802224ab30",
            "total_deliveries": 3,
            "ongoing_deliveries": 2,
            "today_earns": 0.0,
            "this_week_earns": 9702.82,
            "rider_activity": [
                {
                    "id": "35378c22c81e4744aecfb3f38e1f1257",
                    "transaction_type": "CREDIT",
                    "transaction_status": "SUCCESS",
                    "amount": "4851.41",
                    "currency": "₦",
                    "reference": "5up8rw36sul1hlv",
                    "description": None,
                    "created_at": "2024-02-10T23:50:27.131823+01:00",
                },
                {
                    "id": "f51c0e2b81304947a991bc3b86421f0a",
                    "transaction_type": "CREDIT",
                    "transaction_status": "SUCCESS",
                    "amount": "4851.41",
                    "currency": "₦",
                    "reference": "f513fa16336c4ff186a96264227577b2",
                    "description": None,
                    "created_at": "2024-02-10T23:47:47.784923+01:00",
                },
            ],
        },
        "message": "Rider info",
    }
}
RIDER_HOME_RESPONSE = {
    200: openapi.Response(
        description="Rider home", examples=RIDER_HOME_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
RIDER_PERFORMANCE_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "total_delivery": 2,
            "earning": 8926.59,
            "hours_worked": "87 mins",
            "avg_delivery_time": "44 mins",
        },
        "message": "Rider performance",
    }
}
RIDER_PERFORMANCE_RESPONSE = {
    200: openapi.Response(
        description="Rider performance", examples=RIDER_PERFORMANCE_SUCCESS_RESPONSE
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
            "vehicle_id": ["This field is required."],
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
            "vehicle": "CAR (Sedan)",
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
