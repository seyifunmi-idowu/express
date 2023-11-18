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
        description="Retrieved user cards", examples=GET_USER_CARD_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
DEBIT_USER_CARD_RESPONSE_SUCCESS_RESPONSE = {
    "application/json": {
        "data": [
            {"name": "9mobile 9Payment Service Bank", "code": "120001"},
            {"name": "Abbey Mortgage Bank", "code": "404"},
            {"name": "Above Only MFB", "code": "51204"},
            {"name": "Abulesoro MFB", "code": "51312"},
            {"name": "Access Bank", "code": "044"},
            {"name": "Access Bank (Diamond)", "code": "063"},
        ],
        "message": "Card debited",
    }
}
DEBIT_USER_CARD_RESPONSE = {
    200: openapi.Response(description="User card debited", examples={}),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
GET_LIST_OF_BANKS_RESPONSE = {
    200: openapi.Response(
        description="List of banks", examples=DEBIT_USER_CARD_RESPONSE_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
WRONG_ACCOUNT_RESPONSE = {
    "application/json": {"message": "Unable to verify account number"}
}
VERIFY_ACCOUNT_NUMBER_SUCCESS = {
    "application/json": {
        "data": {"account_name": "NIKLAUS MIKAELSON"},
        "message": "Account name",
    }
}
VERIFY_ACCOUNT_NUMBER_RESPONSE = {
    200: openapi.Response(
        description="Account name", examples=VERIFY_ACCOUNT_NUMBER_SUCCESS
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    422: openapi.Response(
        description="Wrong account number", examples=WRONG_ACCOUNT_RESPONSE
    ),
}
INSUFFICIENT_BALANCE = {"application/json": {"message": "Insufficient balance"}}
TRANSFER_FROM_WALLET_BANK_RESPONSE = {
    200: openapi.Response(
        description="Transfer in progress",
        examples={"application/json": {"data": {}, "message": "Transfer in progress"}},
    ),
    400: openapi.Response(
        description="Insufficient balance in account", examples=INSUFFICIENT_BALANCE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    422: openapi.Response(
        description="Wrong account number", examples=WRONG_ACCOUNT_RESPONSE
    ),
}
