# from drf_yasg import openapi

UNAUTHENTICATED = {"application/json": {"message": "Token is invalid or expired"}}
NOT_FOUND = {"application/json": {"message": "Object not found."}}
