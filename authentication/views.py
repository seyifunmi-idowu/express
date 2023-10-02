from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from feleexpress.middlewares.permissions.is_authenticated import IsAuthenticated

from helpers.utils import ResponseManager
from authentication.docs import scehma_doc
from authentication.serializers import UserProfileSerializer


class UserViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        method="get",
        operation_description="Get user",
        operation_summary="Get user",
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
            data=UserProfileSerializer(request.user).data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        method="post",
        operation_description="Logout user",
        operation_summary="Logout user",
        tags=["User"],
        responses=scehma_doc.LOGOUT_RESPONSE,
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="logout",
    )
    def logout(self, request):
        from helpers.token_manager import TokenManager
        access_token = request.auth.token
        TokenManager.logout(access_token)
        return ResponseManager.handle_response(
            data={}, status=status.HTTP_204_NO_CONTENT
        )
