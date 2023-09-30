from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from authentication.docs import scehma_doc
from authentication.service import AuthService
from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager
from rider.serializers import RiderSignupSerializer, VerifyOtpSerializer
from rider.service import RiderService


class RiderAuthViewset(viewsets.ViewSet):
    @swagger_auto_schema(
        methods=["post"],
        request_body=RiderSignupSerializer,
        operation_description="Register a rider",
        operation_summary="Register a rider",
        tags=["Rider-Auth"],
        responses=scehma_doc.RIDER_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="register")
    def signup(self, request):
        serialized_data = RiderSignupSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        RiderService.register_rider(session_id, **serialized_data.data)
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Rider sign up successful"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=VerifyOtpSerializer,
        operation_description="Verify rider otp",
        operation_summary="Verify rider otp",
        tags=["Rider-Auth"],
        responses=scehma_doc.VERIFY_OTP_RESPONSES,
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
