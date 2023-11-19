from drf_yasg import openapi

START_DATE_FILTERS = openapi.Parameter(
    "start_date",
    in_=openapi.IN_QUERY,
    description="Start date for date-range search. The results of the search will include this value",
    type=openapi.TYPE_STRING,
)
END_DATE_FILTERS = openapi.Parameter(
    "end_date",
    in_=openapi.IN_QUERY,
    description="End date for date-range search. The results of the search will include this value",
    type=openapi.TYPE_STRING,
)
TRANSACTION_STATUS = openapi.Parameter(
    "transaction_status",
    in_=openapi.IN_QUERY,
    description="Transaction Status",
    type=openapi.TYPE_STRING,
)
TRANSACTION_TYPE = openapi.Parameter(
    "transaction_type",
    in_=openapi.IN_QUERY,
    description="Transaction type",
    type=openapi.TYPE_STRING,
)
