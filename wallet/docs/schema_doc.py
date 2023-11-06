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
