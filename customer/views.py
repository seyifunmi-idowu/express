from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from authentication.docs.scehma_doc import VERIFY_OTP_RESPONSES
from authentication.service import AuthService
from customer.docs import schema_doc
from customer.serializers import (
    CompleteAuthBusinessCustomerSignupSerializer,
    CompleteBusinessCustomerSignupSerializer,
    CustomerSignupSerializer,
    ResendCustomerVerificationSerializer,
    RetrieveCustomerSerializer,
)
from customer.service import CustomerService
from feleexpress.middlewares.permissions.is_authenticated import (
    IsAuthenticated,
    IsCustomer,
)
from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager
from rider.serializers import (
    FavouriteRiderSerializer,
    RiderLoginSerializer,
    VerifyOtpSerializer,
)


class CustomerAuthViewset(viewsets.ViewSet):
    permission_classes = ()

    @swagger_auto_schema(
        methods=["post"],
        request_body=CustomerSignupSerializer,
        operation_description="Register a customer",
        operation_summary="Register a customer",
        tags=["Customer-Auth"],
        responses=schema_doc.CUSTOMER_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="register")
    def signup(self, request):
        serialized_data = CustomerSignupSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        response = CustomerService.register_customer(session_id, **serialized_data.data)
        return ResponseManager.handle_response(
            data=response,
            status=status.HTTP_200_OK,
            message="Customer sign up successful",
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=CompleteBusinessCustomerSignupSerializer,
        operation_description="Complete business customer registration",
        operation_summary="Complete business customer registration",
        tags=["Customer-Auth"],
        responses=schema_doc.COMPLETE_BUSINESS_CUSTOMER_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="register/complete")
    def complete_business_customer_signup(self, request):
        serialized_data = CompleteBusinessCustomerSignupSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        CustomerService.complete_business_customer_signup(
            session_id, **serialized_data.data
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Customer sign up successful"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=ResendCustomerVerificationSerializer,
        operation_description="Resend verification code",
        operation_summary="Resend verification code",
        tags=["Customer-Auth"],
        responses=schema_doc.CUSTOMER_RESEND_OTP_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="register/resend")
    def resend_verification_code(self, request):
        serialized_data = ResendCustomerVerificationSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        CustomerService.resend_verification_code(session_id, **serialized_data.data)
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Otp sent"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=VerifyOtpSerializer,
        operation_description="Verify customer otp",
        operation_summary="Verify customer otp",
        tags=["Customer-Auth"],
        responses=VERIFY_OTP_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="verify")
    def verify_otp(self, request):
        serialized_data = VerifyOtpSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        phone_number = serialized_data.data.get("phone_number")
        email = serialized_data.data.get("email")
        code = serialized_data.data.get("code")
        if email:
            AuthService.validate_email_verification(
                email=email, code=code, session_id=session_id
            )
        else:
            AuthService.validate_phone_verification(
                phone_number=phone_number, code=code, session_id=session_id
            )

        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Verification successful"
        )

    @swagger_auto_schema(
        method="post",
        request_body=RiderLoginSerializer,
        operation_description="Login a user account with email or phone_number and password",
        operation_summary="Login a User with Basic Authentication - Email or Phone Number",
        tags=["Customer-Auth"],
        responses=schema_doc.LOGIN_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serialized_data = RiderLoginSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )

        session_id = generate_session_id()
        response = CustomerService.customer_login(
            session_id=session_id, **serialized_data.data
        )
        return ResponseManager.handle_response(data=response, status=status.HTTP_200_OK)


class CustomerViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsCustomer)

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get Customer information",
        operation_summary="Get Customer information",
        tags=["Customer"],
        responses=schema_doc.CUSTOMER_INFO_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="info")
    def get_customer_info(self, request):
        rider = CustomerService.get_customer(user=request.user)
        return ResponseManager.handle_response(
            data=RetrieveCustomerSerializer(rider).validated_data,
            status=status.HTTP_200_OK,
            message="Customer info",
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get Customer favourite rider",
        operation_summary="Get Customer favourite rider",
        tags=["Customer"],
        responses=schema_doc.CUSTOMER_FAVOURITE_RIDER_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="favourite-rider")
    def get_customer_favourite_rider(self, request):
        response = CustomerService.get_customer_favourite_rider(user=request.user)
        return ResponseManager.handle_response(
            data=FavouriteRiderSerializer(response, many=True).data,
            status=status.HTTP_200_OK,
            message="Customer favourite rider",
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=CompleteAuthBusinessCustomerSignupSerializer,
        operation_description="Complete business customer registration",
        operation_summary="Complete business customer registration",
        tags=["Customer"],
        responses=schema_doc.COMPLETE_AUTH_BUSINESS_CUSTOMER_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="register/complete")
    def complete_business_customer_signup(self, request):
        serialized_data = CompleteAuthBusinessCustomerSignupSerializer(
            data=request.data
        )
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        CustomerService.complete_business_customer_signup(
            session_id, user=request.user, **serialized_data.validated_data
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Customer sign up successful"
        )
