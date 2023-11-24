from drf_yasg import openapi

UNAUTHENTICATED = {"application/json": {"message": "Token is invalid or expired"}}
NOT_FOUND = {"application/json": {"message": "Object not found."}}

RIDER_INFO_SUCCESS_RESPONSE = {
    "application/json": {
        "data": [
            {
                "id": "8c43444ffbd84074889f0d8dd1447234",
                "name": "Cars (Sedan)",
                "note": None,
                "file_url": None,
            },
            {
                "id": "e4808d9d30f7409085e7bbc59e2f2153",
                "name": "Motorcycle",
                "note": None,
                "file_url": "https://feleexpress.s3.amazonaws.com/backend-dev/available-vehicles/tesla7107aded26d74837b250670564fa1a63.png",
            },
            {
                "id": "dba6af2862574d44bd8e6814f8ba259b",
                "name": "keke",
                "note": None,
                "file_url": None,
            },
        ],
        "message": "Available vehicles",
    }
}
RIDER_INFO_RESPONSE = {
    200: openapi.Response(
        description="Available Vehicles", examples=RIDER_INFO_SUCCESS_RESPONSE
    )
}
