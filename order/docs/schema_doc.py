from drf_yasg import openapi

from order.models import Order

STATUS = openapi.Parameter(
    "status",
    openapi.IN_QUERY,
    description="Filter orders by status",
    type=openapi.TYPE_STRING,
    enum=[stat[0] for stat in Order.STATUS_CHOICES],
)
TIMEFRAME = openapi.Parameter(
    "timeframe",
    openapi.IN_QUERY,
    description="Filter orders by timeframe, yesterday or today",
    type=openapi.TYPE_STRING,
    enum=["today", "yesterday"],
)
CREATED_AT = openapi.Parameter(
    "created_at",
    openapi.IN_QUERY,
    description="Filter orders by created_at (YYYY-MM-DD)",
    type=openapi.TYPE_STRING,
)
UNAUTHENTICATED = {"application/json": {"message": "Token is invalid or expired"}}
NOT_FOUND = {"application/json": {"message": "Object not found."}}
ORDER_NOT_FOUND_RESPONSE = {"application/json": {"message": "Order not found."}}

GET_ALL_ORDER = {
    "application/json": {
        "count": 7,
        "total_pages": 1,
        "current_page": 1,
        "data": [
            {
                "order_id": "glfut9cv8s",
                "status": "ORDER_DELIVERED",
                "pickup": {
                    "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "time": "2024-02-05 09:48:12",
                    "name": "King's Celia Hotels And Suites Jibowu Lagos",
                },
                "delivery": {
                    "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
                    "time": "2024-02-05 09:50:05",
                    "name": "King's Celia Hotels And Suites Jibowu Lagos",
                },
                "rider": {"name": "Messi Messi", "contact": "+2348105474514"},
            },
            {
                "order_id": "rv5p05b82k",
                "status": "PENDING",
                "pickup": {
                    "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "time": None,
                    "name": "King's Celia Hotels And Suites Jibowu Lagos",
                },
                "delivery": {
                    "address": "34 Bajulaye Rd, Igbobi, Lagos 102216, Lagos, Nigeria",
                    "time": None,
                    "name": "King's Celia Hotels And Suites Jibowu Lagos",
                },
                "rider": {"name": None, "contact": None},
            },
        ],
    }
}
GET_ORDER_HISTORY_SUCCESS = {
    "application/json": {
        "count": 7,
        "total_pages": 1,
        "current_page": 1,
        "data": [
            {
                "order_id": "glfut9cv8s",
                "status": "ORDER_DELIVERED",
                "total_amount": "4851.41",
                "pickup": {
                    "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria"
                },
                "delivery": {
                    "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria"
                },
                "rider": {
                    "id": "2c4eccb6025d4c7693c5b9802224ab30",
                    "name": "Messi Messi",
                    "contact": "+2348105474514",
                    "avatar_url": "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/passport_photo/7d09c9a2e6774d0f9ba727c6752f14c2.pdf",
                    "rating": 2.0,
                    "vehicle": "car",
                    "vehicle_type": None,
                    "vehicle_make": None,
                    "vehicle_model": None,
                    "vehicle_plate_number": "eky24sky",
                    "vehicle_color": "red",
                },
                "created_at": "2024-February-04 18:39:17",
                "name": "7 Fola Osibo Rd",
            },
            {
                "order_id": "iwcyiop9kp",
                "status": "RIDER_ACCEPTED_ORDER",
                "total_amount": "4851.41",
                "pickup": {
                    "address": "8 C. A. C St, Ojo, Lagos 102101, Lagos, Nigeria"
                },
                "delivery": {
                    "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria"
                },
                "created_at": "2024-February-04 18:47:11",
                "name": "King's Celia Hotels And Suites Jibowu Lagos",
            },
        ],
    }
}
GET_CUSTOMER_ORDER_SUCCESS = {
    "application/json": {
        "data": {
            "order_id": "glfut9cv8s",
            "status": "ORDER_DELIVERED",
            "payment_method": "WALLET",
            "payment_by": "SENDER",
            "rider": {
                "name": "Messi Messi",
                "contact": "+2348105474514",
                "avatar_url": "https://feleexpress.s3.amazonaws.com/backend-dev/rider_document/passport_photo/7d09c97c6752f14c2.pdf",
                "rating": 2.0,
                "vehicle": "car",
                "vehicle_type": None,
                "vehicle_make": None,
                "vehicle_model": None,
                "vehicle_plate_number": "eky24sky",
                "vehicle_color": "red",
            },
            "rider_contact": "+2348105474514",
            "pickup": {
                "latitude": "6.5358762",
                "longitude": "3.3829932",
                "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                "contact_name": None,
                "contact_phone_number": None,
                "name": "King's Celia Hotels And Suites Jibowu Lagos",
            },
            "delivery": {
                "latitude": "6.5702086",
                "longitude": "3.3509155",
                "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
                "contact_name": None,
                "contact_phone_number": None,
                "name": "7 Fola Osibo Rd",
            },
            "stopover": [
                {
                    "latitude": 6.5304791,
                    "longitude": 3.3786346,
                    "address": "34 Bajulaye Rd, Igbobi, Lagos 102216, Lagos, Nigeria",
                    "contact_name": None,
                    "contact_phone_number": None,
                }
            ],
            "total_amount": "4851.41",
            "tip_amount": None,
            "note_to_driver": "please be fast",
            "distance": "15.6 km",
            "duration": "44 mins",
            "timeline": [
                {
                    "date": "2024-02-04 20:36:33.507815+00:00",
                    "status": "RIDER_ACCEPTED_ORDER",
                },
                {"date": "2024-02-05 09:47:45", "status": "RIDER_AT_PICK_UP"},
                {
                    "date": "2024-02-05 09:48:12",
                    "status": "RIDER_PICKED_UP_ORDER",
                    "proof_of_pickup_url": "https://feleexpress.s3.amazonaws.com/backend-dev/order/glfut9cv8s/e6892e9ae7664bc6a6fa2805d6874081.pdf",
                },
                {"date": "2024-02-05 09:49:48", "status": "ORDER_ARRIVED"},
                {
                    "date": "2024-02-05 09:50:05",
                    "status": "ORDER_DELIVERED",
                    "proof_of_delivery_url": "https://feleexpress.s3.amazonaws.com/backend-dev/order/glfut9cv8s/0a952dc3a4b54bc0825b5baf34a2cff2.pdf",
                },
                {
                    "date": "2024-02-05 09:50:32",
                    "status": "ORDER_DELIVERED",
                    "proof_of_delivery_url": "https://feleexpress.s3.amazonaws.com/backend-dev/order/glfut9cv8s/7ec69823ccd3433c84276fd9938d9131.pdf",
                },
            ],
            "created_at": "2024-02-04 18:39:17",
        },
        "message": "Order Information",
    }
}
CUSTOMER_ORDER_RESPONSE = {
    "order_id": "glfut9cv8s",
    "status": "ORDER_DELIVERED",
    "payment_method": "WALLET",
    "payment_by": "SENDER",
    "pickup": {
        "latitude": 6.6421231,
        "longitude": 3.2779737,
        "address": "2 Church St, Abule Egba, Lagos 102213, Lagos, Nigeria",
        "contact_name": "Tolu",
        "contact_phone_number": "+23412345678",
        "name": "7 Fola Osibo Rd",
    },
    "delivery": {
        "latitude": "6.5702086",
        "longitude": "3.3509155",
        "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
        "contact_name": "John",
        "contact_phone_number": "+23412345678",
        "name": "King's Celia Hotels And Suites Jibowu Lagos",
    },
    "stopover": [
        {
            "latitude": 6.5304791,
            "longitude": 3.3786346,
            "address": "34 Bajulaye Rd, Igbobi, Lagos 102216, Lagos, Nigeria",
            "contact_name": "Son",
            "contact_phone_number": "+23412345678",
        }
    ],
    "total_amount": "4851.41",
    "tip_amount": None,
    "note_to_driver": "please be fast",
    "distance": "15.6 km",
    "duration": "44 mins",
    "timeline": [
        {"date": "2024-02-04 20:36:33.507815+00:00", "status": "RIDER_ACCEPTED_ORDER"},
        {"date": "2024-02-05 09:47:45", "status": "RIDER_AT_PICK_UP"},
        {
            "date": "2024-02-05 09:48:12",
            "status": "RIDER_PICKED_UP_ORDER",
            "proof_of_pickup_url": "https://feleexpress.s3.amazonaws.com/backend-dev/order/glfut9cv8s/e68927664bc6a6fa2805d6874081.pdf",
        },
        {"date": "2024-02-05 09:49:48", "status": "ORDER_ARRIVED"},
        {
            "date": "2024-02-05 09:50:05",
            "status": "ORDER_DELIVERED",
            "proof_of_delivery_url": "https://feleexpress.s3.amazonaws.com/backend-dev/order/glfut9cv8s/0a952dc3a4b55b5baf34a2cff2.pdf",
        },
        {
            "date": "2024-02-05 09:50:32",
            "status": "ORDER_DELIVERED",
            "proof_of_delivery_url": "https://feleexpress.s3.amazonaws.com/backend-dev/order/glfut9cv8s/7ec69823cc4276fd9938d9131.pdf",
        },
    ],
}
RIDER_ORDER_RESPONSE = {
    "data": {
        "order_id": "glfut9cv8s",
        "status": "ORDER_DELIVERED",
        "payment_method": "WALLET",
        "payment_by": "SENDER",
        "pickup": {
            "longitude": "3.3829932",
            "latitude": "6.5358762",
            "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
            "short_address": "24 Olorunkemi Street",
            "complete_address": "Bariga, Lagos 102216, Lagos, Nigeria",
            "contact_name": "Tolu",
            "contact_phone_number": "+23412345678",
            "time": "2024-02-05 09:48:12",
            "name": "King's Celia Hotels And Suites Jibowu Lagos",
        },
        "delivery": {
            "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
            "longitude": "3.3509155",
            "latitude": "6.5702086",
            "short_address": "70 Oduduwa Way",
            "complete_address": "Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
            "contact_name": "Tolu",
            "contact_phone_number": "+23412345678",
            "time": "2024-02-05 09:50:05",
            "name": "King's Celia Hotels And Suites Jibowu Lagos",
        },
        "stopover": [
            {
                "latitude": 6.5304791,
                "longitude": 3.3786346,
                "address": "34 Bajulaye Rd, Igbobi, Lagos 102216, Lagos, Nigeria",
                "contact_name": "Tolu",
                "contact_phone_number": "+23412345678",
            }
        ],
        "total_amount": "4851.41",
        "tip_amount": None,
        "note_to_driver": "please be fast",
        "distance": "15.6 km",
        "duration": "44 mins",
        "created_at": "2024-02-04 18:39:17",
        "contact": {"contact": "", "destination": None},
    },
    "message": "Order Information",
}
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

ADDRESS_INFO_SUCCESS_RESPONSE = {
    "application/json": {
        "data": [
            {
                "name": "Smile View Hotel Extension",
                "latitude": 7.707562899999999,
                "longitude": 8.5194119,
                "formatted_address": "PG59+2QR, Father Hunter Street, High Level, Asuir 970101, Benue, Nigeria",
            },
            {
                "name": "Smile View Hotel Anex",
                "latitude": 7.714796199999999,
                "longitude": 8.513863599999999,
                "formatted_address": "PG77+WGG, Township, Makurdi 970101, Benue, Nigeria",
            },
            {
                "name": "Benue Hotels & Resort",
                "latitude": 7.7350222,
                "longitude": 8.534413899999999,
                "formatted_address": "Benue Hotels and Resort, 57 Ahmadu Bello Way, Old GRA, Makurdi 970101, Benue, Nigeria",
            },
        ],
        "message": "Address information",
    }
}
ADDRESS_INFO_NOT_FOUND_RESPONSE = {
    "application/json": {"message": "Cannot locate address"}
}
ADDRESS_INFO_BAD_REQUEST_RESPONSE = {
    "application/json": {
        "errors": {
            "non_field_errors": [
                "Provide either 'address' or both 'latitude' and 'longitude', but not all three."
            ]
        },
        "message": "",
    }
}
ADDRESS_INFO_RESPONSE = {
    200: openapi.Response(
        description="Address information", examples=ADDRESS_INFO_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad request", examples=ADDRESS_INFO_BAD_REQUEST_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(
        description="Address not found", examples=ADDRESS_INFO_NOT_FOUND_RESPONSE
    ),
}
GET_ORDER_HISTORY_RESPONSE = {
    200: openapi.Response(
        description="Order Information", examples=GET_ORDER_HISTORY_SUCCESS
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
GET_ALL_ORDER_RESPONSE = {
    200: openapi.Response(description="Order Information", examples=GET_ALL_ORDER),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
GET_CUSTOMER_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order Information", examples=GET_CUSTOMER_ORDER_SUCCESS
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
GET_CURRENT_ORDER_SUCCESS_RESPONSE = {
    "application/json": {
        "data": [
            {
                "order_id": "iwcyiop9kp",
                "status": "RIDER_ACCEPTED_ORDER",
                "pickup": {
                    "address": "8 C. A. C St, Ojo, Lagos 102101, Lagos, Nigeria",
                    "longitude": "3.1483086",
                    "latitude": "6.498988799999999",
                    "short_address": "8 C. A. C St",
                    "complete_address": "Ojo, Lagos 102101, Lagos, Nigeria",
                    "contact": "+2348192635372",
                    "contact_name": None,
                    "time": None,
                    "name": "King's Celia Hotels And Suites Jibowu Lagos",
                },
                "delivery": {
                    "address": "70 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
                    "longitude": "3.3509155",
                    "latitude": "6.5702086",
                    "short_address": "70 Oduduwa Way",
                    "complete_address": "Ikeja GRA, Ikeja 101233, Lagos, Nigeria",
                    "contact": "+2348192635372",
                    "contact_name": None,
                    "time": None,
                    "name": "7 Fola Osibo Rd",
                },
                "total_amount": "4851.41",
                "payment_method": None,
                "payment_by": None,
                "distance": "15632",
                "duration": "2614",
                "created_at": "2024-02-04 18:47:11",
                "contact": {"contact": "+2348192635372", "destination": "pickup"},
                "note_to_rider": "",
                "order_by": "Apple",
            },
            {
                "order_id": "2nvdrcz756",
                "status": "RIDER_ACCEPTED_ORDER",
                "pickup": {
                    "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "longitude": "3.3829932",
                    "latitude": "6.5358762",
                    "short_address": "24 Olorunkemi Street",
                    "complete_address": "Bariga, Lagos 102216, Lagos, Nigeria",
                    "contact": "+2348192635372",
                    "contact_name": None,
                    "time": None,
                    "name": "7 Fola Osibo Rd",
                },
                "delivery": {
                    "address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "longitude": "3.3786346",
                    "latitude": "6.5304791",
                    "short_address": "24 Olorunkemi Street",
                    "complete_address": "Bariga, Lagos 102216, Lagos, Nigeria",
                    "contact": "+2348192635372",
                    "contact_name": "John Doe",
                    "time": None,
                    "name": "King's Celia Hotels And Suites Jibowu Lagos",
                },
                "total_amount": "4851.41",
                "payment_method": "CASH",
                "payment_by": "SENDER",
                "distance": "15632",
                "duration": "2614",
                "created_at": "2024-02-05 22:41:05",
                "contact": {"contact": "+2348192635372", "destination": "pickup"},
                "note_to_rider": "please be fast ooooo",
                "order_by": "Chowdeck",
            },
        ],
        "message": "Order Information",
    }
}
GET_CURRENT_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order information", examples=GET_CURRENT_ORDER_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
GET_ORDER_SUCCESS_RESPONSE = {
    "application/json": {
        "data": CUSTOMER_ORDER_RESPONSE,
        "message": "Order Information",
    }
}
GET_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order Information", examples=GET_ORDER_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
CANCEL_CUSTOMER_ORDER_SUCCESS_RESPONSE = {
    "application/json": {"data": {}, "message": "Order cancelled"}
}

CANCEL_CUSTOMER_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order cancelled", examples=CANCEL_CUSTOMER_ORDER_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}

INITIATE_ORDER_SUCCESS_RESPONSE = {
    "application/json": {
        "data": {
            "order_id": "hco2fdce86",
            "pickup": {
                "latitude": 6.5358762,
                "longitude": 3.3829932,
                "save_address": False,
            },
            "delivery": {
                "latitude": 6.5702086,
                "longitude": 3.3509155,
                "save_address": False,
            },
            "stop_overs": [
                {
                    "latitude": 6.554950900000001,
                    "longitude": 3.3663481,
                    "save_address": False,
                }
            ],
            "total_price": 4525.733333333334,
        },
        "message": "Order Information",
    }
}
INITIATE_ORDER_BAD_REQUEST_RESPONSE = {
    "application/json": {
        "errors": {"pickup": {"longitude": ["This field is required."]}},
        "message": "pickup longitude: This field is required.",
    }
}
INITIATE_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order Information", examples=INITIATE_ORDER_SUCCESS_RESPONSE
    ),
    400: openapi.Response(
        description="Bad request", examples=INITIATE_ORDER_BAD_REQUEST_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
}
PLACE_ORDER_SUCCESS_RESPONSE = {
    "application/json": {"data": True, "message": "Finding rider"}
}
PLACE_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order placed successful", examples=PLACE_ORDER_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
ADD_DRIVER_TIP_SUCCESS_RESPONSE = {
    "application/json": {"data": True, "message": "Tip added"}
}
ADD_DRIVER_TIP_RESPONSE = {
    200: openapi.Response(
        description="Tip added", examples=ADD_DRIVER_TIP_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
UNAPPROVED_RIDERS = {
    "application/json": {"message": "Your account has not been approved."}
}
GET_ORDER_SUCCESS_RESPONSE = {
    "application/json": {"data": RIDER_ORDER_RESPONSE, "message": "Order Information"}
}
ACCEPT_CUSTOMER_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order Information", examples=GET_ORDER_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    403: openapi.Response(description="Unapproved Riders", examples=UNAPPROVED_RIDERS),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
RIDER_PICKUP_ORDER_RESPONSE = {
    200: openapi.Response(
        description="Order Information",
        examples={"application/json": {"data": {}, "message": "Order Updated"}},
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    403: openapi.Response(description="Unapproved Riders", examples=UNAPPROVED_RIDERS),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
RIDER_RECEIVE_PAYMENT_RESPONSE = {
    200: openapi.Response(
        description="Order Information",
        examples={
            "application/json": {
                "data": RIDER_ORDER_RESPONSE,
                "message": "Order Updated",
            }
        },
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    403: openapi.Response(description="Unapproved Riders", examples=UNAPPROVED_RIDERS),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
RATE_RIDER_SUCCESS_RESPONSE = {
    "application/json": {"data": True, "message": "Rider rated"}
}
RATE_RIDER_RESPONSE = {
    200: openapi.Response(
        description="Rider rated", examples=RATE_RIDER_SUCCESS_RESPONSE
    ),
    401: openapi.Response(description="Invalid Credentials", examples=UNAUTHENTICATED),
    404: openapi.Response(
        description="Order not found", examples=ORDER_NOT_FOUND_RESPONSE
    ),
}
