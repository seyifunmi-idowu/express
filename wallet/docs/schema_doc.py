from drf_yasg import openapi

UNAUTHENTICATED = {
    "application/json": {"message": "Token is invalid or expired"}  # type: ignore
}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

INITIATE_CARD_TRANSACTION_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {"url": "https://checkout.paystack.com/yyub9pen3ot8my8"},
        "message": "Kyc submitted",
    }
}

INITIATE_CARD_TRANSACTION_RESPONSE = {
    200: openapi.Response(
        description="Card transaction initiated",
        examples=INITIATE_CARD_TRANSACTION_SUCCESS_RESPONSE,
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}

GET_USER_CARD_SUCCESS_RESPONSE = {
    "application/json": {
        "data": [
            {
                "id": "796330929d2646079e73077f41d2fb8d",
                "card_type": "visa ",
                "last_4": "4081",
                "exp_month": "12",
                "exp_year": "2030",
                "country_code": "NG",
                "brand": "visa",
            },
            {
                "id": "98654x29d2646079e73077f41ye83h3i",
                "card_type": "visa ",
                "last_4": "4935",
                "exp_month": "10",
                "exp_year": "2027",
                "country_code": "NG",
                "brand": "visa",
            },
        ],
        "message": "User cards",
    }
}

GET_USER_CARD_RESPONSE = {
    200: openapi.Response(
        description="Retrieved user cards",
        examples=INITIATE_CARD_TRANSACTION_SUCCESS_RESPONSE,
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
