from drf_yasg import openapi

UNAUTHENTICATED = {"application/json": {"message": "Token is invalid or expired"}}
NOT_FOUND = {"application/json": {"message": "notification not found."}}

GET_USER_NOTIFICATION = {
    "application/json": {
        "data": [
            {
                "id": "f1c11589e6214f78a620e5ef06287df9",
                "title": "Pending request",
                "message": "You have a pending order request",
                "created_at": "2024-02-14 17:24:21",
                "opened": False,
            },
            {
                "id": "1005899cd00f4836af0fee6fe15cb4d0",
                "title": "Welcome",
                "message": "Welcome to Fele Express",
                "created_at": "2024-02-14 17:23:50",
                "opened": True,
            },
        ],
        "message": "User notifications",
    }
}
GET_USER_NOTIFICATION_RESPONSE = {
    200: openapi.Response(
        description="User notifications", examples=GET_USER_NOTIFICATION
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
OPENED_USER_NOTIFICATION = {"application/json": {"data": True, "message": "success"}}
OPENED_USER_NOTIFICATION_RESPONSE = {
    200: openapi.Response(
        description="User read notifications", examples=OPENED_USER_NOTIFICATION
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(description="Not found", examples=NOT_FOUND),
}
