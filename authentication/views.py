from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser

from authentication.docs import scehma_doc
from authentication.serializers import (
    ChangePasswordSerializer,
    CustomizeReferralCodeSerializer,
    ForgotPasswordSerializer,
    UserProfileSerializer,
    VerifyForgotPasswordSerializer,
)
from authentication.service import AuthService, UserService
from feleexpress.middlewares.permissions.is_authenticated import IsAuthenticated
from helpers.db_helpers import generate_session_id
from helpers.utils import ResponseManager


def fele_express_api(request):
    response_data = {"status": True, "data": [], "message": "Fele express API"}
    return JsonResponse(response_data)


class UserViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        method="get",
        operation_description="Get user details",
        operation_summary="Get user details",
        tags=["User"],
        responses=scehma_doc.GET_USER_DATA,
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        parser_classes=(MultiPartParser, FormParser),
    )
    def get_user(self, request):
        return ResponseManager.handle_response(
            data=UserProfileSerializer(request.user).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        method="post",
        operation_description="Logout user",
        operation_summary="Logout user",
        tags=["User"],
        responses=scehma_doc.LOGOUT_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        from helpers.token_manager import TokenManager

        access_token = request.auth.token
        TokenManager.logout(access_token)
        return ResponseManager.handle_response(data={}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["post"],
        request_body=ChangePasswordSerializer,
        operation_description="Change password for authenticated user",
        operation_summary="Change password for authenticated user",
        tags=["User"],
        responses=scehma_doc.VERIFY_FORGOT_PASSWORD_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="change/password")
    def change_password(self, request):
        serialized_data = ChangePasswordSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        AuthService.change_password(
            request.user, serialized_data.data, generate_session_id()
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Password changed successful"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=CustomizeReferralCodeSerializer,
        operation_description="Customize user referral code",
        operation_summary="Customize user referral code",
        tags=["User"],
        responses=scehma_doc.GET_USER_DATA,
    )
    @action(detail=False, methods=["post"], url_path="customize-referral-code")
    def customize_referral_code(self, request):
        serialized_data = CustomizeReferralCodeSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = UserService.customize_referral_code(
            request.user,
            serialized_data.validated_data.get("referral_code"),
            generate_session_id(),
        )
        return ResponseManager.handle_response(
            data=UserProfileSerializer(user).data,
            status=status.HTTP_200_OK,
            message="Password changed successful",
        )

    @swagger_auto_schema(
        methods=["delete"],
        operation_description="Delete user",
        operation_summary="Delete user",
        tags=["User"],
        responses=scehma_doc.DELETE_USER,
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_user(self, request):
        UserService.delete_user(request.user)
        return ResponseManager.handle_response(
            data={},
            status=status.HTTP_204_NO_CONTENT,
            message="User deleted successfully",
        )


class AuthViewset(viewsets.ViewSet):
    permission_classes = ()

    @swagger_auto_schema(
        methods=["post"],
        request_body=ForgotPasswordSerializer,
        operation_description="Initiate forgot password reset for unauthenticated user",
        operation_summary="Initiate forgot password reset for unauthenticated user",
        tags=["Auth"],
        responses=scehma_doc.FORGOT_PASSWORD_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="password-reset/initiate")
    def initiate_forgot_password(self, request):
        serialized_data = ForgotPasswordSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = UserService.get_user_instance(serialized_data.data.get("email"))
        AuthService.initiate_email_verification(
            serialized_data.data.get("email"), user.display_name, "Password reset"
        )
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="OTP sent"
        )

    @swagger_auto_schema(
        methods=["post"],
        request_body=VerifyForgotPasswordSerializer,
        operation_description="Verify forgot password reset",
        operation_summary="Verify forgot password reset",
        tags=["Auth"],
        responses=scehma_doc.VERIFY_FORGOT_PASSWORD_RESPONSE,
    )
    @action(detail=False, methods=["post"], url_path="password-reset/verify")
    def verify_forgot_password(self, request):
        serialized_data = VerifyForgotPasswordSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(
                errors=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
            )
        AuthService.verify_forgot_password(serialized_data.data, generate_session_id())
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_200_OK, message="Password reset successful"
        )
