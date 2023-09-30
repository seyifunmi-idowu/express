from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser

from helpers.cache_manager import CacheManager
from helpers.utils import ResponseManager

# Create your views here.


class UserViewset(viewsets.ViewSet):

    # @swagger_auto_schema(
    #     methods=["post"],
    #     request_body=UserAvatarSerializer,
    #     operation_description="Set User Avatar",
    #     operation_summary="Set a User avatar",
    #     tags=["User"],
    #     responses=SET_AVATAR_RESPONSES,
    # )
    @action(
        detail=False,
        methods=["post"],
        url_path="test",
        parser_classes=(MultiPartParser, FormParser),
    )
    def retriever(self, request):
        from helpers.notification import EmailManager, SMSManager
        # result = SMSManager().send_verification_code("+2349112529296")
        # result = SMSManager().new_caller("+2348105474517")
        from helpers.s3_uploader import S3Uploader

        s3_uploader = S3Uploader()

        # Upload the file to S3
        s3_url = s3_uploader.hard_delete_object(
            "https://feleexpress.s3.amazonaws.com/backend-dev/c390e9e4ff354b9ea7c58fd482a8a155.pdf"
        )

        return ResponseManager.handle_response(data={}, status=status.HTTP_200_OK)
