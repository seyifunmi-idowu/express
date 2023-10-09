from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from authentication.docs.scehma_doc import VERIFY_OTP_RESPONSES
from authentication.service import AuthService
from feleexpress.middlewares.permissions.is_authenticated import (
    IsAuthenticated,
    IsRider,
)
from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager
from rider.docs import schema_doc
from rider.serializers import (
    DocumentUploadSerializer,
    KycSerializer,
    RetrieveKycSerializer,
    RetrieveRiderSerializer,
    RiderLoginSerializer,
    RiderSignupSerializer,
    VerifyOtpSerializer,
)
from rider.service import RiderKYCService, RiderService


class RiderAuthViewset(viewsets.ViewSet):
    permission_classes = ()

    @swagger_auto_schema(
        methods=["post"],
        request_body=RiderSignupSerializer,
        operation_description="Register a rider",
        operation_summary="Register a rider",
        tags=["Rider-Auth"],
        responses=schema_doc.RIDER_REGISTRATION_RESPONSES,
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
        tags=["Rider-Auth"],
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
        response = RiderService.rider_login(
            session_id=session_id, **serialized_data.data
        )
        return ResponseManager.handle_response(data=response, status=status.HTTP_200_OK)


class RiderViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider)

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get Rider information",
        operation_summary="Get Rider information",
        tags=["Rider"],
        responses=schema_doc.RIDER_INFO_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="info")
    def get_rider_info(self, request):
        rider = RiderService.get_rider(user=request.user)
        return ResponseManager.handle_response(
            data=RetrieveRiderSerializer(rider).data,
            status=status.HTTP_200_OK,
            message="Rider info",
        )


class RiderKycViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsRider)

    @swagger_auto_schema(
        methods=["post"],
        request_body=KycSerializer,
        operation_description="Submit kyc documents",
        operation_summary="Submit kyc documents",
        tags=["Rider-KYC"],
        responses=schema_doc.SUBMIT_KYC_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="submit")
    def submit_kyc(self, request):
        serialized_data = KycSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        response = RiderKYCService.submit_kyc(
            request.user, session_id, **serialized_data.validated_data
        )
        return ResponseManager.handle_response(
            data=response, status=status.HTTP_200_OK, message="Kyc submitted"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=DocumentUploadSerializer,
        operation_description="Upload kyc documents",
        operation_summary="Upload kyc documents",
        tags=["Rider-KYC"],
        responses=schema_doc.UPLOAD_DOCUMENT_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="upload")
    def upload_document(self, request):
        serialized_data = DocumentUploadSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        session_id = generate_session_id()
        rider = RiderService.get_rider(user=request.user)
        document_type = serialized_data.validated_data.get("document_type")
        documents = serialized_data.validated_data.get("documents")
        for document in documents:
            RiderKYCService.add_rider_document(
                rider=rider,
                document_type=document_type,
                file=document,
                session_id=session_id,
            )

        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Document(s) uploaded"
        )

    @swagger_auto_schema(
        methods=["get"],
        operation_description="Get Kyc information",
        operation_summary="Get Kyc information",
        tags=["Rider-KYC"],
        responses=schema_doc.KYC_INFO_RESPONSE,
    )
    @action(detail=False, methods=["get"], url_path="info")
    def kyc_info(self, request):
        rider = RiderService.get_rider(user=request.user)
        return ResponseManager.handle_response(
            data=RetrieveKycSerializer(rider).data,
            status=status.HTTP_200_OK,
            message="Kyc Info",
        )
